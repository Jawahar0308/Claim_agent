"""
Claims routing logic based on business rules
"""

FRAUD_KEYWORDS = ["fraud", "inconsistent", "staged"]

MANDATORY_FIELDS = [
    "policyNumber",
    "policyholderName",
    "incidentDate",
    "incidentLocation",
    "description",
    "estimatedDamage",
    "claimType"
]


def find_missing_fields(fields: dict) -> list:
    """
    Identify missing mandatory fields.
    
    Args:
        fields: Dictionary of extracted fields
        
    Returns:
        List of missing field names
    """
    missing = []
    for field in MANDATORY_FIELDS:
        if not fields.get(field):
            missing.append(field)
    return missing


def determine_route(fields: dict, missing_fields: list) -> tuple:
    """
    Determine routing decision based on business rules.
    
    Args:
        fields: Dictionary of extracted fields
        missing_fields: List of missing mandatory fields
        
    Returns:
        Tuple of (route, reasoning)
    """
    description = (fields.get("description") or "").lower()
    
    # Rule 1: Check for fraud keywords (highest priority)
    if any(word in description for word in FRAUD_KEYWORDS):
        return "Investigation Flag", f"Suspicious keywords detected in description: {description[:100]}"
    
    # Rule 2: Check for missing mandatory fields
    if missing_fields:
        return "Manual review", f"Missing mandatory fields: {', '.join(missing_fields)}"
    
    # Rule 3: Check if claim involves injury
    if fields.get("claimType") == "injury":
        return "Specialist Queue", "Claim involves injury and requires specialist review"
    
    # Rule 4: Fast-track for low damage amounts
    estimated_damage = fields.get("estimatedDamage")
    if estimated_damage is not None and estimated_damage < 25000:
        return "Fast-track", f"Estimated damage (${estimated_damage:,}) is below $25,000 threshold"
    
    # Default: Manual review
    return "Manual review", "Claim requires standard manual review process"


def process_claim(fields: dict) -> dict:
    """
    Process claim and generate routing decision.
    
    Args:
        fields: Dictionary of extracted fields
        
    Returns:
        Dictionary with routing decision and details
    """
    missing_fields = find_missing_fields(fields)
    route, reasoning = determine_route(fields, missing_fields)
    
    return {
        "extractedFields": fields,
        "missingFields": missing_fields,
        "recommendedRoute": route,
        "reasoning": reasoning
    }
