# coding=utf-8
import logging

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

file_details = {
    "name": {
        "type": "text",
        "fields": {
            "raw": {
                "type": "keyword"
            }
        }
    },
    "file_type": {
        "type": "keyword"
    },
    "owner": {
        "type": "keyword"
    },
    "star": {
        "type": "boolean"
    },
    "description": {
        "type": "text"
    },
    "size": {
        "type": "integer"
    },
    "file_tags": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
            "tag_name": {
                "type": "keyword"
            }
        }
    },
    "created_at": {
        "type": "date",
        "index": False
    },
    "updated_at": {
        "type": "date",
        "index": False
    }
}

sharing_details = {
    "share_mode": {
        "type": "integer"
    },
    "editable": {
        "type": "boolean"
    },
    "users_shared": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
            "user_id": {
                "type": "integer",
            }
        }
    }
}

url_details = {
    "file_id": {
        "type": "keyword"
    },
    "parent_id": {
        "type": "keyword"
    },
    "children_id": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "integer"
            }
        }
    }
}

mappings = {
    "dynamic": "strict",
    "properties": {
        **file_details,
        **sharing_details,
        **url_details
    }
}

settings = {
    "index": {
        "max_result_window": 500000,
        "number_of_shards": "1",
        "analysis": {
            "filter": {
                "synonym_filter": {
                    "type": "synonym",
                    "synonyms": []
                }
            },
            "analyzer": {
                "synonym_analyzer": {
                    "filter": [
                        "lowercase",
                        "synonym_filter"
                    ],
                    "tokenizer": "standard"
                }
            }
        }
    }
}
