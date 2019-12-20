# coding=utf-8
import logging

__author__ = 'jian'
_logger = logging.getLogger(__name__)

NUM_HITS = 10

settings = {
    "analysis": {
        "analyzer": {
            "vn_analyzer": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase"
                ]
            },
            "no_tone_analyzer": {
                "tokenizer": "standard",
                "filter": [
                    "icu_folding",
                    "lowercase"
                ]
            }
        }
    }
}

mappings = {
    "dynamic": "strict",
    "properties": {
        "file_id": {
            "type": "keyword"
        },
        "trashed": {
            "type": "boolean"
        },
        "trashed_time": {
            "type": "date",
            "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
        },
        "file_title": {
            "type": "text",
            "analyzer": "vn_analyzer",
            "fields": {
                'no_tone': {
                    "type": "text",
                    "analyzer": "no_tone_analyzer"
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
        "thumbnail_url": {
            "type": "keyword"
        },
        "parent_id": {
            "type": "keyword"
        },
        "share_mode": {
            "type": "integer"
        },
        "editable": {
            "type": "boolean"
        },
        "users_shared": {
            "type": "keyword"
        },
        "children_id": {
            "type": "keyword"
        },
        "size": {
            "type": "integer"
        },
        "description": {
            "type": "text",
            "analyzer": "vn_analyzer",
            "fields": {
                'no_tone': {
                    "type": "text",
                    "analyzer": "no_tone_analyzer"
                }
            }
        },
        "file_tag": {
            "type": "keyword"
        },
        "created_at": {
            "type": "date",
            "format": "date_optional_time||dd/MM/yyyy hh:mm:ss a"
        },
        "updated_at": {
            "type": "date",
            "format":"date_optional_time||dd/MM/yyyy hh:mm:ss a"
        }
    }
}
