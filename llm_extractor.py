"""
Field extraction using local Ollama LLM (100% FREE)
No API keys, no internet required after setup
"""
import json
import re


def extract_with_llm(text: str) -> dict:
    """
    Extract FNOL fields using local Ollama LLM.
    
    Args:
        text: Raw text from FNOL document
        
    Returns:
        Dictionary with extracted fields
    """
    try:
        from langchain_community.llms import Ollama
        from langchain_core.prompts import PromptTemplate
        
        # Initialize local Ollama LLM
        llm = Ollama(
            model="llama2",
            temperature=0,
            num_predict=512
        )
        
        # Create extraction prompt
        prompt_template = """You are an insurance claims processor. Extract these exact fields from the FNOL document below.
Return ONLY a valid JSON object with these fields:
- policyNumber (string or null)
- policyholderName (string or null)
- incidentDate (string in MM/DD/YYYY format or null)
- incidentLocation (string - city and state or null)
- description (string - brief accident description or null)
- estimatedDamage (integer dollar amount or null)
- claimType (string: "injury", "theft", "fire", or "non-injury")

Do not include any text before or after the JSON. If a field is missing, use null.

FNOL DOCUMENT:
{text}

JSON OUTPUT:"""

        prompt = PromptTemplate(
            input_variables=["text"],
            template=prompt_template
        )
        
        # Limit text length for faster processing
        limited_text = text[:4000] if len(text) > 4000 else text
        
        # Generate response
        print("  Calling local LLM (this may take 10-30 seconds)...")
        response = llm.invoke(prompt.format(text=limited_text))
        print("  ✓ LLM response received")
        
        # Parse JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            fields = json.loads(json_match.group(0))
            print(f"  ✓ Extracted {len([v for v in fields.values() if v])} fields")
            return fields
        else:
            print("  ⚠️ Could not parse JSON from LLM response, using fallback...")
            return fallback_extraction(text)
            
    except ImportError:
        print("  ⚠️ Ollama not installed. Install with:")
        print("     curl -fsSL https://ollama.com/install.sh | sh")
        print("     ollama pull llama2")
        print("  Using fallback regex extraction...")
        return fallback_extraction(text)
        
    except Exception as e:
        print(f"  ⚠️ LLM error: {e}")
        print("  Using fallback regex extraction...")
        return fallback_extraction(text)


def fallback_extraction(text: str) -> dict:
    """
    Fallback regex-based extraction if LLM is not available.
    
    Args:
        text: Raw text from FNOL document
        
    Returns:
        Dictionary with extracted fields
    """
    fields = {}
    
    # Policy information
    fields["policyNumber"] = extract_regex(r"POLICY NUMBER\s*[:\-]?\s*([\w\-]+)", text)
    fields["policyholderName"] = extract_regex(r"NAME OF INSURED\s*\([^)]+\)\s*[:\-]?\s*([A-Za-z][A-Za-z ]+?)(?:\s{2,}|\n|$)", text)
    
    # Incident information
    fields["incidentDate"] = extract_regex(r"DATE OF LOSS[^\n]*?(\d{2}/\d{2}/\d{4})", text)
    fields["incidentLocation"] = extract_regex(r"CITY,\s*STATE(?:,\s*ZIP)?\s*[:\-]?\s*([A-Za-z\s,]+?)(?:\s+\d{5}|\n[A-Z]|\n\n|$)", text)
    fields["description"] = extract_description(text)
    
    # Damage estimate
    fields["estimatedDamage"] = extract_amount(text)
    
    # Claim type
    fields["claimType"] = determine_claim_type(text)
    
    print(f"  ✓ Extracted {len([v for v in fields.values() if v])} fields using fallback")
    
    return fields


def extract_regex(pattern: str, text: str):
    """Extract text using regex pattern."""
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        result = match.group(1).strip()
        result = re.sub(r'\s+', ' ', result)
        return result if result else None
    return None


def extract_description(text: str):
    """Extract accident description."""
    match = re.search(
        r"DESCRIPTION OF ACCIDENT\s*[:\-]?\s*(.*?)(?=POLICE OR FIRE DEPARTMENT|INSURED VEHICLE|WITNESSES|$)",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        result = match.group(1).strip()
        result = re.sub(r'\s+', ' ', result)
        if len(result) > 500:
            result = result[:500]
        return result if result else None
    return None


def extract_amount(text: str):
    """Extract estimated damage amount."""
    match = re.search(r"ESTIMATE AMOUNT\s*[:\-]?\s*\$?(\d+(?:,\d{3})*)", text)
    if match:
        amount_str = match.group(1).replace(',', '')
        return int(amount_str)
    return None


def determine_claim_type(text: str):
    """Determine claim type based on content."""
    text_upper = text.upper()
    
    # Check for actual injury (not just the form label)
    injury_match = re.search(
        r"INJURED\s*[:\-]?\s*(?!NONE)[A-Z]|EXTENT OF INJURY|INJURY\s+TO|INJURED\s+PARTIES",
        text_upper
    )
    if injury_match:
        return "injury"
    
    if re.search(r"\bTHEFT\b|\bSTOLEN\b", text_upper):
        return "theft"
    
    if re.search(r"\bFIRE\b(?!\s+DEPARTMENT)", text_upper):
        return "fire"
    
    return "non-injury"
