curl -XPUT 'localhost:9200/zadolbali' -H 'Content-Type: application/json' -d'
{
    "mappings": {
        "stories": {
            "properties": {
                "id": { "type": "integer" },
                "title":  { "type": "text" },
                "text": { "type": "text" },
                "published": {
                    "type": "date",
                    "format": "yyyyMMdd"
                    },
                "likes": { "type": "integer" },
                "tags": { "type": "text" },
                "url": { "type": "text" }
                }
            }
        }
    }
}
'