"""
Context processor for handling user permissions and roles in Django templates.

This module provides a context processor that automatically makes user permissions
and roles available in all Django templates, enabling template-level access control.
"""

from users.models import UserRole

def get_permissions(request):
    """
    Context processor that provides user permissions and roles to templates.
    
    This function is automatically called by Django for every request and adds
    the 'permissions' and 'roles' variables to the template context.
    
    Args:
        request: Django HTTP request object containing user information
        
    Returns:
        dict: Dictionary containing:
            - permissions: Dict mapping module names to permission levels (0-3)
            - roles: List of role names assigned to the current user
            
    Permission levels:
        0: No access
        1: Read-only access
        2: Read and write access
        3: Full access (including delete/admin)
        
    Modules covered:
        - customer: Customer management permissions
        - supliers: Supplier management permissions  
        - materials: Material/inventory item permissions
        - purchases: Purchase order permissions
        - sales: Sales order permissions
        - inventory: Inventory management permissions
        - accounting: Financial/accounting permissions
        - reporting: Report generation permissions
    """
    # Initialize permissions dictionary with all modules set to 0 (no access)
    permissions = {
        'customer': 0,
        'suppliers': 0,  # Note: likely typo, should be 'suppliers'
        'materials': 0,
        'purchases': 0,
        'sales': 0,
        'inventory': 0,
        'accounting': 0,
        'reporting': 0,
    }

    # Initialize empty roles list
    roles = []

    # Only process if user is authenticated
    if request.user.is_authenticated:
        # Get all UserRole objects for the current user
        user_roles = UserRole.objects.filter(user_id=request.user.pk)

        # Extract role names from UserRole objects
        roles = [ur.role.role_name for ur in user_roles]
        
        # Process permissions for each user role
        for user_role in user_roles:
            role = user_role.role
            # Check each module's permission level for this role
            for module in permissions.keys():
                # Get permission level for this module (default to 0 if not found)
                current_permission = getattr(role, module, 0)
                # Use the highest permission level if user has multiple roles
                if current_permission > permissions[module]:
                    permissions[module] = current_permission

    # Return context data for templates
    return {
        'permissions': permissions,  # Dict of module permissions
        'roles': roles               # List of user's role names
    }
