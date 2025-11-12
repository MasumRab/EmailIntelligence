"""
AI Response Parser - Minimal parsing
"""

import json
import structlog

logger = structlog.get_logger()


class AIResponseParser:
    @staticmethod
    def parse(response):
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if content.strip().startswith("{"):
                return json.loads(content)
            
            # Find JSON in content
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1:
                return json.loads(content[start:end])
            
            return {"error": "No JSON found", "content": content}
        except:
            return {"error": "Parse failed"}


    @staticmethod
    def fictionality(response, context, hash_id):
        data = AIResponseParser.parse(response)
        score = data.get("fictionality_score", 0.5)
        
        return {
            "id": f"fic_{hash_id}",
            "score": score,
            "indicators": data.get("fictionality_indicators", []),
            "reasoning": data.get("reasoning", ""),
            "fallback": "parse_failed" in data
        }


    @staticmethod
    def conflict(response, pr_data, conflict_data, analysis_id):
        data = AIResponseParser.parse(response)
        return {
            **data,
            "id": analysis_id,
            "pr_id": pr_data.get("id"),
            "conflicts": len(conflict_data.get("conflicts", []))
        }