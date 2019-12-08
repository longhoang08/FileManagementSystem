# coding=utf-8
import logging

__author__ = 'jian'
_logger = logging.getLogger(__name__)

NUM_HITS = 10

index_config = {
    "settings": {
        "analysis": {
            "analyzer": {
                "ngram_analyzer": {
                    "tokenizer": "ngram_tokenizer",
                    "filter": [
                        "lowercase"
                    ]
                }
            },
            "tokenizer": {
                "ngram_tokenizer": {
                    "type": "ngram",
                    "min_gram": 3,
                    "max_gram": 3,
                    "token_chars": [
                        "letter",
                        "digit",
                        "punctuation",
                        "symbol"
                    ]
                }
            }
        }
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "file_id": {
                "type": "keyword"
            },
            "file_title": {
                "type": "text",
                "analyzer": "ngram_analyzer"
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
                "analyzer": "ngram_analyzer"
            },
            "file_tag": {
                "type": "keyword"
            },
            "created_at": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            },
            "updated_at": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            }
        }
    }
}
