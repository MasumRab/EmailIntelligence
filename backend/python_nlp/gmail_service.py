    async def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get detailed performance metrics for Gmail operations.

        Returns comprehensive performance data including sync times, success rates,
        error rates, and resource usage tracking.
        """
        try:
            # Get current timestamp for metrics
            current_time = datetime.now()

            # Calculate performance metrics from stats
            total_operations = self.stats.get("total_sync_operations", 0)
            successful_operations = self.stats.get("successful_sync_operations", 0)
            failed_operations = self.stats.get("failed_sync_operations", 0)

            # Calculate success rate
            success_rate = (
                (successful_operations / total_operations * 100) if total_operations > 0 else 0
            )

            # Calculate average sync time
            total_sync_time = self.stats.get("total_sync_time_seconds", 0)
            avg_sync_time = total_sync_time / total_operations if total_operations > 0 else 0

            # Get API usage metrics
            api_calls_made = self.stats.get("api_calls_made", 0)
            rate_limit_hits = self.stats.get("rate_limit_hits", 0)

            # Get resource usage
            emails_processed = self.stats.get("emails_processed", 0)
            data_processed_mb = self.stats.get("data_processed_bytes", 0) / (
                1024 * 1024
            )  # Convert to MB

            # Build comprehensive performance metrics
            performance_metrics = {
                "summary": {
                    "total_sync_operations": total_operations,
                    "successful_operations": successful_operations,
                    "failed_operations": failed_operations,
                    "success_rate_percent": round(success_rate, 2),
                    "average_sync_time_seconds": round(avg_sync_time, 2),
                    "total_emails_processed": emails_processed,
                    "total_data_processed_mb": round(data_processed_mb, 2),
                },
                "api_usage": {
                    "total_api_calls": api_calls_made,
                    "rate_limit_hits": rate_limit_hits,
                    "api_call_efficiency": round(api_calls_made / max(emails_processed, 1), 2),
                },
                "performance_trends": {
                    "last_sync_time": self.stats.get("last_sync_timestamp"),
                    "average_response_time_ms": self.stats.get("avg_response_time_ms", 0),
                    "peak_sync_duration_seconds": self.stats.get("peak_sync_duration", 0),
                },
                "error_analysis": {
                    "error_rate_percent": round(
                        (failed_operations / max(total_operations, 1)) * 100, 2
                    ),
                    "common_error_types": self.stats.get("error_types", {}),
                    "last_error_timestamp": self.stats.get("last_error_timestamp"),
                },
                "resource_usage": {
                    "bandwidth_used_mb": round(data_processed_mb, 2),
                    "processing_efficiency": round(
                        emails_processed / max(total_sync_time, 1), 2
                    ),  # emails/second
                    "memory_peak_usage_mb": self.stats.get("memory_peak_mb", 0),
                },
                "timestamp": current_time.isoformat(),
                "status": "active" if self.stats.get("service_active", True) else "inactive",
            }

            return performance_metrics

        except Exception as e:
            self.logger.error(f"Error retrieving performance metrics: {e}")
            return {
                "error": f"Failed to retrieve performance metrics: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "status": "error",
            }

    async def execute_smart_retrieval(
        self, strategies: List[str] = None, max_api_calls: int = 100, time_budget_minutes: int = 30
    ) -> Dict[str, Any]:
        """
        Args:
            strategies: A list of retrieval strategies to execute.
            max_api_calls: The maximum number of API calls allowed.
            time_budget_minutes: The time budget in minutes for the process.

        Returns:
            A dictionary with the results of the retrieval process.
        """
        cmd = [
            sys.executable,
            self.retrieval_script,
            "execute-strategies",
            "--max-api-calls",
            str(max_api_calls),
            "--time-budget",
            str(time_budget_minutes),
        ]
        if strategies:
            cmd.extend(["--strategies"] + strategies)
        return await self._execute_async_command(cmd, cwd=self.nlp_path)

    async def get_retrieval_strategies(self) -> List[Dict[str, Any]]:
        """
        Retrieves available email retrieval strategies.

        Returns:
            A list of dictionaries representing available retrieval strategies.
        """
        # Implementation would go here
        return []


async def main():
    """
    Demonstrates the usage of the GmailAIService.
    """
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    service = GmailAIService()
    sync_result = await service.sync_gmail_emails(max_emails=2)
    logging.info(f"Sync result: {sync_result}")


if __name__ == "__main__":
    asyncio.run(main())
=======
>>>>>>> origin/main
