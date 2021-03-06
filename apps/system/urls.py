from django.urls import path

from .views import SystemView,SystemSetupView
from . import views_structure, views_user, views_menu, views_role,views_cameraset,views_worktimeset

app_name = 'system'

urlpatterns = [
    path('', SystemView.as_view(), name='login'),
    path('basic/structure/', views_structure.StructureView.as_view(), name='basic-structure'),
    path('basic/structure/create/', views_structure.StructureCreateView.as_view(), name='basic-structure-create'),
    path('basic/structure/list/', views_structure.StructureListView.as_view(), name='basic-structure-list'),
    path('basic/structure/delete/', views_structure.StructureDeleteView.as_view(), name='basic-structure-delete'),
    path('basic/structure/add_user/', views_structure.Structure2UserView.as_view(), name='basic-structure-add_user'),

    path('basic/cameraset/', views_cameraset.CameraSetView.as_view(), name='basic-camera'),
    path('basic/cameraset/create/', views_cameraset.CameraSetCreateView.as_view(), name='basic-camera-create'),
    path('basic/cameraset/list/', views_cameraset.CameraSetListView.as_view(), name='basic-camera-list'),
    path('basic/cameraset/delete/', views_cameraset.CameraSetDeleteView.as_view(), name='basic-camera-delete'),

	path('basic/worktimeset/', views_worktimeset.WorktimeSetView.as_view(), name='basic-worktime'),
    path('basic/worktimeset/create/', views_worktimeset.WorktimeSetCreateView.as_view(), name='basic-worktime-create'),
    path('basic/worktimeset/list/', views_worktimeset.WorktimeSetListView.as_view(), name='basic-worktime-list'),
    path('basic/worktimeset/delete/', views_worktimeset.WorktimeSetDeleteView.as_view(), name='basic-worktime-delete'),

    path('basic/structure/addclient/', views_structure.AddClientView.as_view(), name='addclient'),
    path('basic/structure/deleteclient/', views_structure.DeleteClientView.as_view(), name='deleteclient'),
    path('basic/structure/updateclient/', views_structure.UpdateClientView.as_view(), name='updateclient'),

    path('basic/user/', views_user.UserView.as_view(), name='basic-user'),
    path('basic/user/list/', views_user.UserListView.as_view(), name='basic-user-list'),
    path('basic/user/create/', views_user.UserCreateView.as_view(), name='basic-user-create'),
    path('basic/user/detail/', views_user.UserDetailView.as_view(), name='basic-user-detail'),
    path('basic/user/update/', views_user.UserUpdateView.as_view(), name='basic-user-update'),
    path('basic/user/password_change/', views_user.PasswordChangeView.as_view(), name='basic-user-password_change'),
    path('basic/user/delete/', views_user.UserDeleteView.as_view(), name='basic-user-delete'),
    path('basic/user/enable/', views_user.UserEnableView.as_view(), name='basic-user-enable'),
    path('basic/user/disable/', views_user.UserDisableView.as_view(), name='basic-user-disable'),

    path('rbac/menu/', views_menu.MenuListView.as_view(), name='rbac-menu'),
    path('rbac/menutree/', views_menu.MenuTree.as_view(), name='rbac-menu'),
    path('rbac/menu/create/', views_menu.MenuCreateView.as_view(), name='rbac-menu-create'),
    path('rbac/menu/update/', views_menu.MenuUpdateView.as_view(), name='rbac-menu-update'),

    path('rbac/role/', views_role.RoleView.as_view(), name='rbac-role'),
    path('rbac/role/create/', views_role.RoleCreateView.as_view(), name='rbac-role-create'),
    path('rbac/role/list/', views_role.RoleListView.as_view(), name='rbac-role-list'),
    path('rbac/role/update/', views_role.RoleUpdateView.as_view(), name='rbac-role-update'),
    path('rbac/role/delete/', views_role.RoleDeleteView.as_view(), name='rbac-role-delete'),
    path('rbac/role/role2user/', views_role.Role2UserView.as_view(), name="rbac-role-role2user"),
    path('rbac/role/role2menu/', views_role.Role2MenuView.as_view(), name="rbac-role-role2menu"),
    path('rbac/role/role2menu_list/', views_role.Role2MenuListView.as_view(), name="rbac-role-role2menu_list"),

    path('tools/system_setup/', SystemSetupView.as_view(), name="system_setup"),
]
