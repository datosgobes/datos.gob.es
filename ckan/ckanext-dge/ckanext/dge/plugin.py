# Copyright (C) 2017 Entidad P�blica Empresarial Red.es
# 
# This file is part of "ckanext-dge (datos.gob.es)".
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckanext.scheming.helpers as sh
import ckanext.dge_scheming.helpers as dsh
import ckan.model as model
import pylons
from pylons import config
from ckanext.dge import helpers
from ckanext.dge.helpers import TRANSLATED_UNITS as TRANSLATED_UNITS
from ckanext.dge.helpers import DEFAULT_UNIT as DEFAULT_UNIT
from collections import OrderedDict
from routes.mapper import SubMapper
from ckan.lib.plugins import DefaultTranslation
import ckan.logic as logic
import ckan.logic.auth as logic_auth
import ckan.logic.action as logic_action
import ckan.authz as authz
from ckan.common import _
import ckan.lib.base as base
import ckan.lib.plugins as lib_plugins
import ckan.lib.dictization.model_dictize as model_dictize

import logging

log = logging.getLogger(__name__)
is_frontend = False

@toolkit.auth_allow_anonymous_access
def dge_organization_publisher(context, data_dict=None):
    try:
        model = context['model']
        id = logic.get_or_bust(data_dict, 'id')
        group = model.Group.get(id)
        context['group'] = group
        if group is None:
            raise NotFound
        if not group.is_organization:
            raise NotFound
        group_dict = model_dictize.group_dictize(group, context,
                                                 packages_field='dataset_count',
                                                 include_tags=False,
                                                 include_extras=True,
                                                 include_groups=False,
                                                 include_users=False,)
        group_plugin = lib_plugins.lookup_group_plugin(group_dict['type'])
        schema = logic.schema.default_show_group_schema()
        group_dict, errors = lib_plugins.plugin_validate(
            group_plugin, context, group_dict, schema,
            'organization_show')
        return group_dict
    except:
        return {}

#@toolkit.auth_allow_anonymous_access
def dge_organization_show(context, data_dict=None):
    authorized = True
    user = context['user']
    group = logic_auth.get_group_object(context, data_dict)
    if group:
        # Get list of organizations in which the user can show.
        orgs = toolkit.get_action('organization_list_for_user')(data_dict={'permission': 'read'})
        if orgs:
             org_ids = [org_tuple['id'] for org_tuple in orgs]
             authorized = True if group.id in org_ids else False
    if not authorized:
        return {'success': False,
             'msg': _('User %s not authorized to edit organization %s') %
                         (user, group.id)}
    else:
        return {'success': True}

def dge_harvest_source_show(context, data_dict=None):
    authorized = False
    user = context['user']
    package_id = data_dict['id']
    owner_org = data_dict['owner_org']
    orgs = toolkit.get_action('organization_list_for_user')(data_dict={'permission': 'read'})
    if orgs:
        org_ids = [org_tuple['id'] for org_tuple in orgs]
        authorized = True if owner_org in org_ids else False
    if not authorized:
        return {'success': False,
                 'msg': _('User %s not authorized to show harvest source %s') %
                             (user, package_id)}
    else:
        return {'success': True}

def is_frontend():
    is_frontend = False
    config_is_frontend = config.get('ckanext.dge.is_frontend', None)
    if config_is_frontend and config_is_frontend.lower() == 'true': 
        is_frontend = True  
    return is_frontend

class DgePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)

    if is_frontend(): 
        log.debug('IS_FRONTEND')
        plugins.implements(plugins.ITranslation, inherit=True)
        plugins.implements(plugins.IConfigurer, inherit=True)
        plugins.implements(plugins.IAuthFunctions, inherit=True)
        plugins.implements(plugins.IFacets, inherit=True)
        plugins.implements(plugins.IRoutes, inherit=True)
        plugins.implements(plugins.IActions, inherit=True)

    # ############### IActions ############################################## #

    def get_actions(self):
        if not is_frontend():
            return {}
        return {'dge_organization_publisher' : dge_organization_publisher,}

    # ############### IAuthFunctions ######################################### #

    def get_auth_functions(self):
        if not is_frontend():
            return {}

        unauthorized = lambda context, data_dict: {'success': False}
        authorized = lambda context, data_dict: {'success': True}
        return {
            'organization_show': dge_organization_show,
            'dge_harvest_source_show': dge_harvest_source_show,
            'dge_organization_publisher': authorized,
            }

    # ############### IConfigurer ############################################ #

    def update_config(self, config_):
        if is_frontend():
            toolkit.add_template_directory(config_, 'templates')
            toolkit.add_public_directory(config_, 'public')
            toolkit.add_resource('fanstatic', 'dge')

    # ############### IFacets ################################################ #

    #Remove group facet
    def _facets(self, facets_dict):
        if is_frontend():
            if 'group' in facets_dict:
                del facets_dict['group']
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        if not is_frontend():
            return facets_dict

        lang_code = pylons.request.environ['CKAN_LANG']
        facets_dict.clear()
        facets_dict['theme_id'] = plugins.toolkit._('Category')
        facets_dict['res_format_label'] = plugins.toolkit._('Format')
        facets_dict['publisher_display_name'] = plugins.toolkit._('Publisher')
        facets_dict['tags'] = plugins.toolkit._('Tag')
        facets_dict['administration_level'] = plugins.toolkit._('Administration level')
        return self._facets(facets_dict)

    def group_facets(self, facets_dict, group_type, package_type):
        if not is_frontend():
            return facets_dict
        
        return self._facets(facets_dict)

    def organization_facets(self, facets_dict, organization_type, package_type):
        if not is_frontend():
            return facets_dict
        
        lang_code = pylons.request.environ['CKAN_LANG']
        facets_dict.clear()
        facets_dict['organization'] = plugins.toolkit._('Organization') 
        facets_dict['theme_id'] =  plugins.toolkit._('Category')
        facets_dict['res_format_label'] = plugins.toolkit._('Format')
        facets_dict['publisher_display_name'] = plugins.toolkit._('Publisher')
        facets_dict['tags'] = plugins.toolkit._('Tag')
        facets_dict['administration_level'] = plugins.toolkit._('Administration level')
        return self._facets(facets_dict)

    # ############### ITemplateHelpers ####################################### #

    def get_helpers(self):
        return {
            'dge_default_locale': helpers.dge_default_locale,
            'dge_dataset_field_value': helpers.dge_dataset_field_value,
            'dge_dataset_display_fields': helpers.dge_dataset_display_fields,
            'dge_render_datetime': helpers.dge_render_datetime,
            'dge_is_downloadable_resource': helpers.dge_is_downloadable_resource,
            'dge_dataset_display_name': helpers.dge_dataset_display_name,
            'dge_resource_display_name': helpers.dge_resource_display_name,
            'dge_get_dataset_publisher': helpers.dge_get_dataset_publisher,
            'dge_get_organization_administration_level_code': helpers.dge_get_organization_administration_level_code,
            'dge_get_dataset_administration_level': helpers.dge_get_dataset_administration_level,
            'dge_list_reduce_resource_format_label': helpers.dge_list_reduce_resource_format_label,
            'dge_theme_id': helpers.dge_theme_id,
            'dge_list_themes': helpers.dge_list_themes,
            'dge_dataset_display_frequency': helpers.dge_dataset_display_frequency,
            'dge_url_for_user_organization': helpers.dge_url_for_user_organization,
            'dge_resource_display_name_or_desc': helpers.dge_resource_display_name_or_desc,
            'dge_package_list_for_source': helpers.dge_package_list_for_source,
            'dge_api_swagger_url': helpers.dge_api_swagger_url,
            'dge_sparql_yasgui_endpoint': helpers.dge_sparql_yasgui_endpoint,
            'dge_resource_format_label': helpers.dge_resource_format_label,
            'dge_exported_catalog_files': helpers.dge_exported_catalog_files,
            'dge_get_endpoints_menu': helpers.dge_get_endpoints_menu,
            'dge_sort_alphabetically_resources': helpers.dge_sort_alphabetically_resources,
            'dge_dataset_tag_list_display_names': helpers.dge_dataset_tag_list_display_names,
            'dge_swagger_doc_url': helpers.dge_swagger_doc_url,
            'dge_sparql_yasgui_doc_url': helpers.dge_sparql_yasgui_doc_url,
            }

    # ############### IRoutes ################################################ #

    def _common_map(self, _map):
        try:
            log.debug("_from_dataset_to_catalogo")
            
            #from /dataset to /catalogo
            with SubMapper(_map, controller='error') as m:
                 m.connect('/catalogo/{action}/{id}/{revision}', action='read_ajax',
                          requirements=dict(action='|'.join([
                              'history',
                          ])))
                 m.connect('/catalogo/{action}/{id}',
                          requirements=dict(action='|'.join([
                              'history',
                              'history_ajax',
                              'follow',
                              'activity',
                              'groups',
                              'unfollow',
                          ])))
                 m.connect('dataset_followers', '/catalogo/followers/{id}',
                          action='followers', ckan_icon='group')
                 m.connect('dataset_activity', '/catalogo/activity/{id}',
                          action='activity', ckan_icon='time')
                 m.connect('/catalogo/activity/{id}/{offset}', action='activity')
                 m.connect('dataset_groups', '/catalogo/groups/{id}',
                          action='groups', ckan_icon='group')
                 m.connect('/catalogo/{id}/resource/{resource_id}/embed',
                          action='resource_embedded_dataviewer')
                 m.connect('/catalogo/{id}/resource/{resource_id}/viewer',
                          action='resource_embedded_dataviewer', width="960",
                          height="800")
                 m.connect('/catalogo/{id}/resource/{resource_id}/preview',
                          action='resource_datapreview')
                 m.connect('views', '/catalogo/{id}/resource/{resource_id}/views',
                          action='resource_views', ckan_icon='reorder')
                 m.connect('new_view', '/catalogo/{id}/resource/{resource_id}/new_view',
                          action='edit_view', ckan_icon='edit')
                 m.connect('edit_view',
                          '/catalogo/{id}/resource/{resource_id}/edit_view/{view_id}',
                          action='edit_view', ckan_icon='edit')
                 m.connect('resource_view',
                          '/catalogo/{id}/resource/{resource_id}/view/{view_id}',
                          action='resource_view')
                 m.connect('/catalogo/{id}/resource/{resource_id}/view/',
                          action='resource_view')
 
            with SubMapper(_map, controller='package') as m:
                m.connect('search', '/catalogo', action='search',
                          highlight_actions='index search')
                m.connect('add dataset', '/catalogo/new', action='new')
                m.connect('/catalogo/{action}',
                          requirements=dict(action='|'.join([
                              'list',
                              'autocomplete',
                              'search'
                          ])))
 
                m.connect('/catalogo/{action}/{id}/{revision}', action='read_ajax',
                          requirements=dict(action='|'.join([
                              'read',
                              'edit'
                          ])))
                m.connect('/catalogo/{action}/{id}',
                          requirements=dict(action='|'.join([
                              'new_resource',
                              'read_ajax',
                              'delete',
                              'api_data',
                          ])))
                m.connect('dataset_edit', '/catalogo/edit/{id}', action='edit',
                          ckan_icon='edit') 
                m.connect('dataset_resources', '/catalogo/resources/{id}',
                          action='resources', ckan_icon='reorder')
                m.connect('dataset_read', '/catalogo/{id}', action='read',
                          ckan_icon='sitemap')
                m.connect('/catalogo/{id}/resource/{resource_id}',
                          action='resource_read')
                m.connect('/catalogo/{id}/resource_delete/{resource_id}',
                          action='resource_delete')
                m.connect('resource_edit', '/catalogo/{id}/resource_edit/{resource_id}',
                          action='resource_edit', ckan_icon='edit')
                m.connect('/catalogo/{id}/resource/{resource_id}/download',
                          action='resource_download')
                m.connect('/catalogo/{id}/resource/{resource_id}/download/{filename}',
                          action='resource_download')


            with SubMapper(_map, controller='ckanext.dge.controllers:DGEPackageController') as m:
                m.connect('harvest_search', '/harvest', action='search')
                m.connect('harvest_new', '/harvest/new', action='new')
                m.connect('harvest_read', '/harvest/{id}', action='read')
                m.connect('harvest_history', '/harvest/history{id}', action='history')
                m.connect('harvest_authz', '/harvest/authz/{id}', action='authz')

            

        except Exception as e:
            log.warn("_from_dataset_to_catalogo exception %r: %r:", type(e), e.message)
        return _map
    
    def before_map(self, _map):
        if not is_frontend():
            return _map

        try:
            log.debug("before_map")

            with SubMapper(_map, controller='ckanext.dge.controllers:DGEController') as m:
                m.connect('yasgui', '/sparql', action='yasgui')
                m.connect('accessible_yasgui', '/accessible-sparql', action='accessible_yasgui')
                m.connect('apidata', '/apidata', action='swagger')
                m.connect('accessible_apidata', '/accessible-apidata', action='accessible_swagger')
                m.connect('organism', '/recurso/sector-publico/org/Organismo', action='organism')
                m.connect('spatial_coverage', '/recurso/sector-publico/territorio/{type}/{name}', action='spatial_coverage')
                m.connect('theme', '/kos/sector-publico/sector/{name}', action='theme')

            with SubMapper(_map, controller='ckanext.dge.controllers:DGEUtilController') as m:
                m.connect('/util/redirect_search', action='redirect_search')

            #Redirect package to catalogo
            _map.redirect('/packages', '/catalogo')
            _map.redirect('/packages/{url:.*}', '/catalogo/{url}')
            _map.redirect('/package', '/catalogo')
            _map.redirect('/package/{url:.*}', '/catalogo/{url}')
            _map.redirect('/dataset', '/catalogo')
            _map.redirect('/dataset/{url:.*}', '/catalogo/{url}')
            _map = self._common_map(_map)
            
            # group
            _map.redirect('/groups', '/group')
            _map.redirect('/groups/{url:.*}', '/group/{url}')

            # These named routes are used for custom group forms which will use the
            # names below based on the group.type ('group' is the default type)
            with SubMapper(_map, controller='error') as m:
                m.connect('group_index', '/group', action='index',
                          highlight_actions='index search')
                m.connect('group_list', '/group/list', action='list')
                m.connect('group_new', '/group/new', action='new')
                m.connect('group_action', '/group/{action}/{id}',
                          requirements=dict(action='|'.join([
                              'edit',
                              'delete',
                              'member_new',
                              'member_delete',
                              'history',
                              'followers',
                              'follow',
                              'unfollow',
                              'admins',
                              'activity',
                           ])))
                m.connect('group_about', '/group/about/{id}', action='about',
                          ckan_icon='info-sign'),
                m.connect('group_edit', '/group/edit/{id}', action='edit',
                          ckan_icon='edit')
                m.connect('group_members', '/group/members/{id}', action='members',
                          ckan_icon='group'),
                m.connect('group_activity', '/group/activity/{id}/{offset}',
                          action='activity', ckan_icon='time'),
                m.connect('group_read', '/group/{id}', action='read',
                          ckan_icon='sitemap')
            with SubMapper(_map, controller='error') as m:
                m.connect('/organization/list', action='list')
                m.connect('/organization/new', action='new')
                m.connect('/organization/{action}/{id}',
                          requirements=dict(action='|'.join([
                              'delete',
                              'admins',
                              'member_new',
                              'member_delete',
                              'history'
                          ])))
                m.connect('organization_activity', '/organization/activity/{id}/{offset}',
                          action='activity', ckan_icon='time')
                m.connect('organization_about', '/organization/about/{id}',
                          action='about', ckan_icon='info-sign')
                m.connect('organization_edit', '/organization/edit/{id}',
                          action='edit', ckan_icon='edit')
                m.connect('organization_members', '/organization/members/{id}',
                          action='members', ckan_icon='group')
                m.connect('organization_bulk_process',
                          '/organization/bulk_process/{id}',
                          action='bulk_process', ckan_icon='sitemap')
            # organizations these basically end up being the same as groups
            with SubMapper(_map, controller='organization') as m:
                m.connect('organization_read', '/organization/{id}', action='read')
                m.connect('organization_read', '/organization/{id}', action='read',
                          ckan_icon='sitemap')

            with SubMapper(_map, controller='ckanext.dge.controllers:DGEOrganizationController') as m:
                m.connect('organizations_index', '/organization', action='index')
    
            #other hidding pages
            _map.redirect('/', '/catalogo')
            _map.connect('about', '/about', action='about')
            
             # tags
            _map.connect('/tag', controller='error', action='index')
            _map.connect('/tag/{id}', controller='error', action='read')

            #user
            with SubMapper(_map, controller='error') as m:
                m.connect('register', '/user/register', action='register')
                m.connect('login', '/user/login', action='login')
                m.connect('/user/_logout', action='logout')
                m.connect('/user/logged_in', action='logged_in')
                m.connect('/user/logged_out', action='logged_out')
                m.connect('/user/logged_out_redirect', action='logged_out_page')

            # group
            _map.redirect('/dashboard', '/catalogo')
            _map.redirect('/dashboard/{url:.*}', '/catalogo/{url}')
            
            with SubMapper(_map, controller='error') as m:
                m.connect('/user/edit', action='edit')
                # Note: openid users have slashes in their ids, so need the wildcard
                # in the route.
                m.connect('user_generate_apikey', '/user/generate_key/{id}', action='generate_apikey')
                m.connect('/user/activity/{id}/{offset}', action='activity')
                m.connect('user_activity_stream', '/user/activity/{id}',
                          action='activity', ckan_icon='time')
                m.connect('user_dashboard', '/dashboard', action='dashboard',
                          ckan_icon='list')
                m.connect('user_dashboard_datasets', '/dashboard/datasets',
                          action='dashboard_datasets', ckan_icon='sitemap')
                m.connect('user_dashboard_groups', '/dashboard/groups',
                          action='dashboard_groups', ckan_icon='group')
                m.connect('user_dashboard_organizations', '/dashboard/organizations',
                          action='dashboard_organizations', ckan_icon='building')
                m.connect('/dashboard/{offset}', action='dashboard')
                m.connect('user_follow', '/user/follow/{id}', action='follow')
                m.connect('/user/unfollow/{id}', action='unfollow')
                m.connect('user_followers', '/user/followers/{id:.*}',
                          action='followers', ckan_icon='group')
                m.connect('user_edit', '/user/edit/{id:.*}', action='edit',
                          ckan_icon='cog')
                m.connect('user_delete', '/user/delete/{id}', action='delete')
                m.connect('/user/reset/{id:.*}', action='perform_reset')
                m.connect('/user/reset', action='request_reset')
                m.connect('/user/me', action='me')
                m.connect('/user/set_lang/{lang}', action='set_lang')
                m.connect('user_datasets', '/user/{id:.*}', action='read',
                          ckan_icon='sitemap')
                m.connect('user_index', '/user', action='index')

            with SubMapper(_map, controller='error') as m:
                m.connect('/revision', action='index')
                m.connect('/revision/edit/{id}', action='edit')
                m.connect('/revision/diff/{id}', action='diff')
                m.connect('/revision/list', action='list')
                m.connect('/revision/{id}', action='read')

            # feeds
            with SubMapper(_map, controller='ckanext.dge.controllers:DGEFeedController') as m:
                m.connect('/feeds/dataset.atom', action='general')

            with SubMapper(_map, controller='error') as m:
                m.connect('/feeds/group/{id}.atom', action='group')
                m.connect('/feeds/organization/{id}.atom', action='organization')
                m.connect('/feeds/tag/{id}.atom', action='tag')
                #m.connect('/feeds/dataset.atom', action='general')
                m.connect('/feeds/custom.atom', action='custom')

            _map.connect('ckanadmin_index', '/ckan-admin', controller='error',
                        action='index', ckan_icon='legal')
            _map.connect('ckanadmin_config', '/ckan-admin/config', controller='error',
                        action='config', ckan_icon='check')
            _map.connect('ckanadmin_trash', '/ckan-admin/trash', controller='error',
                        action='trash', ckan_icon='trash')
            _map.connect('ckanadmin', '/ckan-admin/{action}', controller='error')

            with SubMapper(_map, controller='error') as m:
                m.connect('storage_file', '/storage/f/{label:.*}',
                          action='file')

            with SubMapper(_map, controller='util') as m:
                m.connect('/i18n/strings_{lang}.js', action='i18n_js_strings')
                m.connect('/util/redirect', action='redirect')
              
            with SubMapper(_map, controller='error') as m:
                m.connect('/i18n/strings_{lang}.js', action='i18n_js_strings')
                m.connect('/util/redirect', action='redirect')
           
        except Exception as e:
            log.warn("MAP Before_map exception %r: %r:", type(e), e.message)
        return _map

    def after_map(self, _map):
        
        if not is_frontend():
            return _map

        _map = self._common_map(_map)

        return _map    

    # ############### IPackageController ##################################### #

    def before_index(self, data_dict):
        dataset = sh.scheming_get_schema('dataset', 'dataset')
        if ('res_format' in data_dict):
            #Get format field
            formats = sh.scheming_field_by_name(dataset.get('resource_fields'),
                            'format')
 
            #Create SOLR field
            data_dict['res_format_label'] = []
            for res_format in data_dict['res_format']:
                #Get format label
                res_format_label = sh.scheming_choices_label(formats['choices'], res_format)
                if res_format_label:
                    #Add label to new SOLR field
                    data_dict['res_format_label'].append(res_format_label)
 
        if ('publisher' in data_dict):
            organismo = data_dict['publisher']
            if is_frontend():
                publisher = toolkit.get_action('dge_organization_publisher')({'model': model}, {'id': organismo})
            else:
                publisher = h.get_organization(organismo)
            data_dict['publisher'] = publisher.get('id')
            data_dict['publisher_display_name'] = publisher.get('display_name')
            administration_level_code = helpers.dge_get_organization_administration_level_code(publisher)
            if not administration_level_code or administration_level_code not in TRANSLATED_UNITS:
                administration_level_code = DEFAULT_UNIT
            data_dict['administration_level'] = administration_level_code
            data_dict['administration_level_es'] = TRANSLATED_UNITS[administration_level_code]['es'] or ''
            data_dict['administration_level_en'] = TRANSLATED_UNITS[administration_level_code]['en'] or ''
            data_dict['administration_level_ca'] = TRANSLATED_UNITS[administration_level_code]['ca'] or ''
            data_dict['administration_level_eu'] = TRANSLATED_UNITS[administration_level_code]['eu'] or ''
            data_dict['administration_level_gl'] = TRANSLATED_UNITS[administration_level_code]['gl'] or ''
 
        if ('theme' in data_dict):
            #Get theme field
            categoria = sh.scheming_field_by_name(dataset.get('dataset_fields'),
                            'theme')
 
            #Get theme value
            valor_categoria = data_dict['theme']
 
            #Empty theme values
            data_dict['theme'] = []
            data_dict['theme_id'] = []
            data_dict['theme_es'] = []
            data_dict['theme_en'] = []
            data_dict['theme_ca'] = []
            data_dict['theme_eu'] = []
            data_dict['theme_gl'] = []
 
            #Get key values
            valores = valor_categoria.replace('[','').replace(']','')
            categorias = valores.split('", "')
            #Get translated label for each key
            for term_categoria in list(categorias):
                clean_term = term_categoria.replace('"','')
                data_dict['theme'].append(clean_term)
                data_dict['theme_id'].append(helpers.dge_theme_id(clean_term))
                #Look for label in the scheme
                for option in categoria.get('choices'):
                    if option['value'] == clean_term:
                        #Add label for each language
                        data_dict['theme_es'].append(option['label']['es'])
                        data_dict['theme_en'].append(option['label']['en'])
                        data_dict['theme_ca'].append(option['label']['ca'])
                        data_dict['theme_eu'].append(option['label']['eu'])
                        data_dict['theme_gl'].append(option['label']['gl'])
        return data_dict

    def before_search(self, search_params):        
        if not is_frontend():
            return search_params

        order_by = search_params.get('sort', '')
        if not order_by:
            search_params['sort'] = 'metadata_modified desc'

        fq = search_params.get('fq', '')
        if fq and fq.find(u'+dataset_type:harvest') > -1:
            orgs = toolkit.get_action('organization_list_for_user')(data_dict={'permission': 'read'})
            if orgs:
                org_ids = ''
                for org_tuple in orgs:
                    org_ids = '{0} OR {1}'.format(org_ids, org_tuple['id'])
                if len(org_ids) > 4:
                    org_ids = org_ids[4:]
                    fq = '{0} +owner_org:({1})'.format(fq, org_ids)
                else:
                    fq = '{0} -owner_org:[\'\' TO *]'.format(fq, '')
            else:
                fq = '{0} -owner_org:[\'\' TO *]'.format(fq, '')
            search_params.update({'fq': fq})
        
        search_params['defType'] = ''
        return search_params

    def after_search(self, search_results, search_params):
        if not is_frontend():
            return search_results

       # Translate the unselected search facets.
        facets = search_results.get('search_facets')
        if not facets:
            return search_results

        desired_lang_code = pylons.request.environ['CKAN_LANG']
        fallback_lang_code = pylons.config.get('ckan.locale_default', 'es')

        # Look up translations for all of the facets in one db query.
        dataset = sh.scheming_get_schema('dataset', 'dataset')
        categoria = sh.scheming_field_by_name(dataset.get('dataset_fields'), 'theme')
        dict_categoria = {}
        for option in categoria.get('choices'):
            label_option = (option.get('label')).get(desired_lang_code, None)
            if not label_option:
                 label_option = (option.get('label')).get(fallback_lang_code, None)
            dict_categoria[helpers.dge_theme_id(option.get('value'))] = label_option
        facet = facets.get('theme_id', None)
        if facet:
            for item in facet.get('items', None):
                item['display_name'] = dict_categoria.get(item.get('name'), item.get('display_name'))
                item['class'] = item.get('name')
        
        facet = facets.get('administration_level', None)
        if facet:
            for item in facet.get('items', None):
                item['display_name'] = helpers.dge_get_translated_administration_level(item.get('name'))
        return search_results