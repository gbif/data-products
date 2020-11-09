{
	"_source": {
		"includes": ["title", "description", "_score", "samplingDescription"],
		"excludes": ["geographicCoverages"]
	},
	"size": 2000,
	"query": {
		"bool": {
			"should": [{
				"wildcard": {
					"title": {
						"value": "corer?",
						"rewrite": "scoring_boolean"
					}
				}
			}, {
				"wildcard": {
					"description": {
						"value": "corer?",
						"rewrite": "scoring_boolean"
					}
				}
			}, {
				"wildcard": {
					"samplingDescription": {
						"value": "corer?",
						"rewrite": "scoring_boolean"
					}
				}
			}, {
				"wildcard": {
					"title": {
						"value": "trawl?",
						"rewrite": "scoring_boolean"
					}
				}
			}, {
				"wildcard": {
					"description": {
						"value": "trawl?",
						"rewrite": "scoring_boolean"
					}
				}
			}, {
				"wildcard": {
					"samplingDescription": {
						"value": "trawl?",
						"rewrite": "scoring_boolean"
					}
				}
			}]
		}
	}
}