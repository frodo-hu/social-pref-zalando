# rules_engine/schema.py

"""
Define the JSON schema for layout rules:
- highlightProducts: list of product IDs to bump to the top
- themeColors: primary/secondary for header/footer
"""
layout_schema = {
    "type": "object",
    "properties": {
        "highlightProducts": {
            "type": "array",
            "items": { "type": "string" }
        },
        "themeColors": {
            "type": "object",
            "properties": {
                "primary": { "type": "string" },
                "secondary": { "type": "string" }
            },
            "required": ["primary", "secondary"]
        }
    },
    "required": ["highlightProducts", "themeColors"]
}