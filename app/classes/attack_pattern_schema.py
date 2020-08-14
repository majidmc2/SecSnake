AttackPatternSchema = {
    "type": "object",
    "properties": {
        "configuration": {
            "type": "object",
            "properties": {
                "interval": {"type": "number"},
                "thread": {"type": "number"}
            },
            "additionalProperties": False
        },

        "interaction_monitoring": {
            "type": "object",
            "properties": {
                "element": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "tag": {"type": "string"},
                            "attribute": {"type": "string"},
                            "check": {
                                "type": "object",
                                "properties": {
                                    "regexp": {"type": "string"},
                                    "data": {"type": "string"}
                                }
                            }
                        },
                        "additionalProperties": False,
                        "required": ["tag", "attribute", "check"]
                    }
                },

                "css": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "tag": {"type": "string"},
                            "property": {"type": "string"},
                            "check": {
                                "type": "object",
                                "properties": {
                                    "if_equal": {"type": ["number", "string"]},
                                    "if_lees_than": {"type": "number"},
                                    "if_more_than": {"type": "number"}
                                }
                            }
                        },
                        "additionalProperties": False,
                        "required": ["tag", "property", "check"]
                    }
                },

                "javascript": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string"}
                    },
                    "required": ["pattern"]
                }
            },
            "additionalProperties": False
        },

        "on_before_request": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "beacon",
                            "csp_report",
                            "font",
                            "image",
                            "imageset",
                            "main_frame",
                            "object_subrequest",
                            "ping",
                            "script",
                            "speculative",
                            "stylesheet",
                            "sub_frame",
                            "web_manifest",
                            "websocket",
                            "xbl",
                            "xml_dtd",
                            "xmlhttprequest",
                            "xslt"
                        ]
                    }
                },
                "method": {"type": "array"},
                "url": {
                    "type": "object",
                    "properties": {
                        "regexp": {"type": "string"},
                        "data": {"type": "string"}
                    }
                },
                "decode_url": {"type": "boolean"},
                "document_url": {"type": "boolean"},
                "origin_url": {"type": "boolean"},
                "main_frame": {"type": "boolean"},
                "parent_frame": {"type": "boolean"}
            },
            "additionalProperties": False,
            "required": ["origin_url"]
        }
    }
}
