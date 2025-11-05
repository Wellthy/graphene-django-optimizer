"""
Tests for SQL injection vulnerability fixes.
Tests for the _connector SQL injection vulnerability (CVE-2024-XXXXX).
"""
import pytest
from django.db.models import Q
from graphene_django_optimizer.utils import sanitize_queryset_kwargs
from tests.models import Item


class TestConnectorSQLInjection:
    """
    Test that the _connector SQL injection vulnerability is fixed.
    
    The vulnerability allows SQL injection when using dictionary expansion
    with the _connector argument in QuerySet.filter(), exclude(), or get().
    """

    def test_sanitize_queryset_kwargs_removes_connector(self):
        """Test that _connector is removed from kwargs."""
        kwargs = {"name": "test", "_connector": "malicious"}
        sanitized = sanitize_queryset_kwargs(kwargs)
        
        assert "_connector" not in sanitized
        assert sanitized["name"] == "test"
        assert len(sanitized) == 1

    def test_sanitize_queryset_kwargs_preserves_valid_keys(self):
        """Test that valid keys are preserved."""
        kwargs = {"name": "test", "value__gte": 10, "parent__name": "parent"}
        sanitized = sanitize_queryset_kwargs(kwargs)
        
        assert sanitized == kwargs
        assert len(sanitized) == 3

    def test_sanitize_queryset_kwargs_handles_empty_dict(self):
        """Test that empty dict is handled correctly."""
        kwargs = {}
        sanitized = sanitize_queryset_kwargs(kwargs)
        
        assert sanitized == {}

    def test_sanitize_queryset_kwargs_handles_none(self):
        """Test that None is handled correctly."""
        sanitized = sanitize_queryset_kwargs(None)
        assert sanitized is None

    def test_sanitize_queryset_kwargs_handles_non_dict(self):
        """Test that non-dict values are returned as-is."""
        value = "not a dict"
        sanitized = sanitize_queryset_kwargs(value)
        assert sanitized == value

    def test_sanitize_queryset_kwargs_only_connector(self):
        """Test that kwargs with only _connector returns empty dict."""
        kwargs = {"_connector": "malicious"}
        sanitized = sanitize_queryset_kwargs(kwargs)
        
        assert "_connector" not in sanitized
        assert len(sanitized) == 0

    @pytest.mark.django_db
    def test_filter_with_sanitized_kwargs_prevents_injection(self):
        """
        Test that using sanitized kwargs prevents SQL injection.
        This simulates an attack attempt using _connector.
        """
        # Create test data
        Item.objects.create(name="test1", value=10)
        Item.objects.create(name="test2", value=20)
        
        # Simulate potentially malicious user input
        user_input = {
            "name": "test1",
            "_connector": "OR 1=1"  # Simulated SQL injection attempt
        }
        
        # Sanitize the input before using in filter
        sanitized = sanitize_queryset_kwargs(user_input)
        
        # This should work without raising an exception or SQL injection
        results = Item.objects.filter(**sanitized)
        
        # Should only return the item with name="test1"
        assert results.count() == 1
        assert results.first().name == "test1"

    @pytest.mark.django_db
    def test_filter_with_connector_nested_in_lookups(self):
        """
        Test that _connector in nested lookups is not a problem when using
        standard lookup syntax (not expansion).
        """
        Item.objects.create(name="test1", value=10)
        
        # Using standard lookups (not dictionary expansion) is safe
        results = Item.objects.filter(name="test1", value__gte=5)
        
        assert results.count() == 1
        assert results.first().name == "test1"

    def test_sanitize_preserves_original_dict(self):
        """Test that sanitization doesn't modify the original dictionary."""
        original = {"name": "test", "_connector": "malicious"}
        original_copy = original.copy()
        
        sanitized = sanitize_queryset_kwargs(original)
        
        # Original should be unchanged
        assert original == original_copy
        assert "_connector" in original
        
        # Sanitized should have _connector removed
        assert "_connector" not in sanitized
