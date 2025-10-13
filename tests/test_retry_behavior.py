"""Unit tests for retry behavior and configuration"""

from unittest.mock import AsyncMock, call, patch

import pytest

from app.utils.retry import (
    NO_RETRY_CONFIG,
    READ_RETRY_CONFIG,
    WRITE_RETRY_CONFIG,
    RetryConfig,
    retry_async,
    retry_none,
    retry_read,
    retry_with_backoff,
    retry_write,
)


class TestRetryConfig:
    """Test RetryConfig class"""

    def test_default_config(self):
        """Test default configuration values"""
        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.base_delay == 0.1
        assert config.max_delay == 2.0
        assert config.backoff_factor == 2.0
        assert config.jitter is True
        assert config.retryable_exceptions == (ConnectionError, TimeoutError, OSError)

    def test_custom_config(self):
        """Test custom configuration values"""
        config = RetryConfig(
            max_attempts=5,
            base_delay=0.5,
            max_delay=3.0,
            backoff_factor=1.5,
            jitter=False,
            retryable_exceptions=(ValueError,)
        )
        assert config.max_attempts == 5
        assert config.base_delay == 0.5
        assert config.max_delay == 3.0
        assert config.backoff_factor == 1.5
        assert config.jitter is False
        assert config.retryable_exceptions == (ValueError,)


class TestRetryWithBackoff:
    """Test retry_with_backoff function"""

    @pytest.mark.asyncio
    async def test_success_on_first_attempt(self):
        """Test successful execution on first attempt"""
        mock_func = AsyncMock(return_value="success")

        result = await retry_with_backoff(
            mock_func,
            config=READ_RETRY_CONFIG,
            operation_name="test_operation"
        )

        assert result == "success"
        assert mock_func.call_count == 1

    @pytest.mark.asyncio
    async def test_retry_success_after_failures(self):
        """Test successful retry after initial failures"""
        mock_func = AsyncMock(side_effect=[ConnectionError("fail"), ConnectionError("fail"), "success"])

        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            result = await retry_with_backoff(
                mock_func,
                config=READ_RETRY_CONFIG,
                operation_name="test_operation"
            )

        assert result == "success"
        assert mock_func.call_count == 3
        assert mock_sleep.call_count == 2  # Should sleep before retries 2 and 3

    @pytest.mark.asyncio
    async def test_retry_exhausted_raises_last_exception(self):
        """Test that exhausted retries raise the last exception"""
        mock_func = AsyncMock(side_effect=[ConnectionError("fail1"), ConnectionError("fail2"), ConnectionError("fail3")])

        with patch('asyncio.sleep', new_callable=AsyncMock):
            with pytest.raises(ConnectionError, match="fail3"):
                await retry_with_backoff(
                    mock_func,
                    config=READ_RETRY_CONFIG,
                    operation_name="test_operation"
                )

        assert mock_func.call_count == 3

    @pytest.mark.asyncio
    async def test_non_retryable_exception_fails_immediately(self):
        """Test that non-retryable exceptions fail immediately"""
        mock_func = AsyncMock(side_effect=ValueError("non-retryable"))

        with pytest.raises(ValueError, match="non-retryable"):
            await retry_with_backoff(
                mock_func,
                config=READ_RETRY_CONFIG,
                operation_name="test_operation"
            )

        assert mock_func.call_count == 1

    @pytest.mark.asyncio
    async def test_backoff_delay_calculation(self):
        """Test exponential backoff delay calculation"""
        mock_func = AsyncMock(side_effect=[ConnectionError("fail"), "success"])

        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await retry_with_backoff(
                mock_func,
                config=READ_RETRY_CONFIG,
                operation_name="test_operation"
            )

        # Should calculate delay: base_delay * (backoff_factor ** (attempt_index - 1))
        # For the second attempt (attempt_index = 2): 0.1 * (2.0 ** 0) = 0.1 before jitter
        mock_sleep.assert_called_once()
        delay_arg = mock_sleep.call_args[0][0]
        assert 0.07 <= delay_arg <= 0.13  # Allow for ±25% jitter

    @pytest.mark.asyncio
    async def test_jitter_disabled(self):
        """Test behavior when jitter is disabled"""
        config = RetryConfig(jitter=False, base_delay=0.1, backoff_factor=2.0)
        mock_func = AsyncMock(side_effect=[ConnectionError("fail"), "success"])

        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await retry_with_backoff(
                mock_func,
                config=config,
                operation_name="test_operation"
            )

        # Without jitter: delay should be exactly base_delay for the first retry
        mock_sleep.assert_called_once_with(0.1)

    @pytest.mark.asyncio
    async def test_max_delay_limit(self):
        """Test that delay never exceeds max_delay"""
        config = RetryConfig(
            max_attempts=4,
            base_delay=1.0,
            max_delay=1.5,
            backoff_factor=3.0,
            jitter=False
        )
        mock_func = AsyncMock(side_effect=[ConnectionError("fail"), ConnectionError("fail"), "success"])

        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await retry_with_backoff(
                mock_func,
                config=config,
                operation_name="test_operation"
            )

        # Delays should be: 1.0, min(1.0 * 3.0, 1.5) = 1.5
        expected_calls = [call(1.0), call(1.5)]
        mock_sleep.assert_has_calls(expected_calls)


class TestRetryDecorator:
    """Test retry_async decorator"""

    @pytest.mark.asyncio
    async def test_decorator_success(self):
        """Test decorator with successful function"""
        @retry_async(config=READ_RETRY_CONFIG, operation_name="decorated_func")
        async def test_func():
            """
            Provide a sentinel success value used by decorator tests.
            
            Returns:
                str: The sentinel value "decorated_success".
            """
            return "decorated_success"

        result = await test_func()
        assert result == "decorated_success"

    @pytest.mark.asyncio
    async def test_decorator_retry(self):
        """Test decorator with retry"""
        @retry_async(config=READ_RETRY_CONFIG, operation_name="decorated_func")
        async def test_func():
            test_func.call_count += 1
            if test_func.call_count < 3:
                raise ConnectionError("fail")
            return "retry_success"

        test_func.call_count = 0

        with patch('asyncio.sleep', new_callable=AsyncMock):
            result = await test_func()

        assert result == "retry_success"
        assert test_func.call_count == 3

    @pytest.mark.asyncio
    async def test_decorator_auto_operation_name(self):
        """Test decorator auto-generates operation name"""
        @retry_async(config=READ_RETRY_CONFIG)
        async def test_func():
            return "success"

        with patch('app.utils.retry.logger') as mock_logger:
            await test_func()

        # Should log with auto-generated operation name
        mock_logger.debug.assert_not_called()  # No retries, so no debug logs

    def test_predefined_decorators(self):
        """Test predefined decorators exist and have correct configs"""
        assert retry_read is not None
        assert retry_write is not None
        assert retry_none is not None

        # Verify they have different configs by checking their closure
        # This is a bit of a hack to access the config from the decorator
        import inspect

        # Get the config from retry_read decorator
        retry_read_source = inspect.getsource(retry_read)
        assert "READ_RETRY_CONFIG" in retry_read_source

        retry_write_source = inspect.getsource(retry_write)
        assert "WRITE_RETRY_CONFIG" in retry_write_source

        retry_none_source = inspect.getsource(retry_none)
        assert "NO_RETRY_CONFIG" in retry_none_source


class TestLoggingBehavior:
    """Test logging behavior during retries"""

    @pytest.mark.asyncio
    async def test_retry_logging(self):
        """Test that retry attempts are logged correctly"""
        mock_func = AsyncMock(side_effect=[ConnectionError("fail"), "success"])

        with patch('asyncio.sleep', new_callable=AsyncMock):
            with patch('app.utils.retry.logger') as mock_logger:
                await retry_with_backoff(
                    mock_func,
                    config=READ_RETRY_CONFIG,
                    operation_name="test_operation"
                )

        # Should log warning for failure and info for success
        mock_logger.warning.assert_called_once()
        warning_call = mock_logger.warning.call_args
        assert "test_operation failed on attempt 1" in warning_call[0][0]
        assert warning_call[1]["extra"]["retry"] is True

        mock_logger.info.assert_called_once()
        info_call = mock_logger.info.call_args
        assert "test_operation succeeded on attempt 2" in info_call[0][0]
        assert info_call[1]["extra"]["retry"] is True

    @pytest.mark.asyncio
    async def test_exhausted_retry_logging(self):
        """Test logging when all retries are exhausted"""
        mock_func = AsyncMock(side_effect=[ConnectionError("fail1"), ConnectionError("fail2")])

        with patch('asyncio.sleep', new_callable=AsyncMock):
            with patch('app.utils.retry.logger') as mock_logger:
                try:
                    await retry_with_backoff(
                        mock_func,
                        config=RetryConfig(max_attempts=2),
                        operation_name="test_operation"
                    )
                except ConnectionError:
                    pass  # Expected

        # Should log error for exhaustion
        mock_logger.error.assert_called_once()
        error_call = mock_logger.error.call_args
        assert "test_operation failed after 2 attempts" in error_call[0][0]
        assert error_call[1]["extra"]["retry"] is True

    @pytest.mark.asyncio
    async def test_non_retryable_logging(self):
        """Test logging for non-retryable exceptions"""
        mock_func = AsyncMock(side_effect=ValueError("non-retryable"))

        with patch('app.utils.retry.logger') as mock_logger:
            try:
                await retry_with_backoff(
                    mock_func,
                    config=READ_RETRY_CONFIG,
                    operation_name="test_operation"
                )
            except ValueError:
                pass  # Expected

        # Should log error for non-retryable exception
        mock_logger.error.assert_called_once()
        error_call = mock_logger.error.call_args
        assert "non-retryable error" in error_call[0][0]
        assert error_call[1]["extra"]["retry"] is False


class TestPredefinedConfigs:
    """Test predefined retry configurations"""

    def test_read_config(self):
        """Test READ_RETRY_CONFIG has appropriate values"""
        assert READ_RETRY_CONFIG.max_attempts == 3
        assert READ_RETRY_CONFIG.base_delay == 0.1
        assert READ_RETRY_CONFIG.max_delay == 1.0
        assert READ_RETRY_CONFIG.jitter is True

    def test_write_config(self):
        """Test WRITE_RETRY_CONFIG has appropriate values"""
        assert WRITE_RETRY_CONFIG.max_attempts == 2
        assert WRITE_RETRY_CONFIG.base_delay == 0.2
        assert WRITE_RETRY_CONFIG.max_delay == 1.5
        assert WRITE_RETRY_CONFIG.jitter is True

    def test_no_retry_config(self):
        """Test NO_RETRY_CONFIG has appropriate values"""
        assert NO_RETRY_CONFIG.max_attempts == 1
        assert NO_RETRY_CONFIG.base_delay == 0.0
        assert NO_RETRY_CONFIG.max_delay == 0.0
        assert NO_RETRY_CONFIG.jitter is False
