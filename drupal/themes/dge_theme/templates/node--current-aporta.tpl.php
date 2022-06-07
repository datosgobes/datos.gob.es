<?php

/**
 	* Copyright (C) 2022 Entidad Pública Empresarial Red.es
 	*
 	* This file is part of "dge_theme (datos.gob.es)".
 	*
 	* This program is free software: you can redistribute it and/or modify
 	* it under the terms of the GNU General Public License as published by
 	* the Free Software Foundation, either version 2 of the License, or
 	* (at your option) any later version.
 	*
 	* This program is distributed in the hope that it will be useful,
 	* but WITHOUT ANY WARRANTY; without even the implied warranty of
 	* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 	* GNU General Public License for more details.
 	*
 	* You should have received a copy of the GNU General Public License
 	* along with this program. If not, see <http://www.gnu.org/licenses/>.
 	*/

/**
 * @file
 * Default theme implementation to display a node.
 *
 * Available variables:
 * - $title: the (sanitized) title of the node.
 * - $content: An array of node items. Use render($content) to print them all,
 *   or print a subset such as render($content['field_example']). Use
 *   hide($content['field_example']) to temporarily suppress the printing of a
 *   given element.
 * - $user_picture: The node author's picture from user-picture.tpl.php.
 * - $date: Formatted creation date. Preprocess functions can reformat it by
 *   calling format_date() with the desired parameters on the $created variable.
 * - $name: Themed username of node author output from theme_username().
 * - $node_url: Direct URL of the current node.
 * - $display_submitted: Whether submission information should be displayed.
 * - $submitted: Submission information created from $name and $date during
 *   template_preprocess_node().
 * - $classes: String of classes that can be used to style contextually through
 *   CSS. It can be manipulated through the variable $classes_array from
 *   preprocess functions. The default values can be one or more of the
 *   following:
 *   - node: The current template type; for example, "theming hook".
 *   - node-[type]: The current node type. For example, if the node is a
 *     "Blog entry" it would result in "node-blog". Note that the machine
 *     name will often be in a short form of the human readable label.
 *   - node-teaser: Nodes in teaser form.
 *   - node-preview: Nodes in preview mode.
 *   The following are controlled through the node publishing options.
 *   - node-promoted: Nodes promoted to the front page.
 *   - node-sticky: Nodes ordered above other non-sticky nodes in teaser
 *     listings.
 *   - node-unpublished: Unpublished nodes visible only to administrators.
 * - $title_prefix (array): An array containing additional output populated by
 *   modules, intended to be displayed in front of the main title tag that
 *   appears in the template.
 * - $title_suffix (array): An array containing additional output populated by
 *   modules, intended to be displayed after the main title tag that appears in
 *   the template.
 *
 * Other variables:
 * - $node: Full node object. Contains data that may not be safe.
 * - $type: Node type; for example, story, page, blog, etc.
 * - $comment_count: Number of comments attached to the node.
 * - $uid: User ID of the node author.
 * - $created: Time the node was published formatted in Unix timestamp.
 * - $classes_array: Array of html class attribute values. It is flattened
 *   into a string within the variable $classes.
 * - $zebra: Outputs either "even" or "odd". Useful for zebra striping in
 *   teaser listings.
 * - $id: Position of the node. Increments each time it's output.
 *
 * Node status variables:
 * - $view_mode: View mode; for example, "full", "teaser".
 * - $teaser: Flag for the teaser state (shortcut for $view_mode == 'teaser').
 * - $page: Flag for the full page state.
 * - $promote: Flag for front page promotion state.
 * - $sticky: Flags for sticky post setting.
 * - $status: Flag for published status.
 * - $comment: State of comment settings for the node.
 * - $readmore: Flags true if the teaser content of the node cannot hold the
 *   main body content.
 * - $is_front: Flags true when presented in the front page.
 * - $logged_in: Flags true when the current user is a logged-in member.
 * - $is_admin: Flags true when the current user is an administrator.
 *
 * Field variables: for each field instance attached to the node a corresponding
 * variable is defined; for example, $node->body becomes $body. When needing to
 * access a field's raw values, developers/themers are strongly encouraged to
 * use these variables. Otherwise they will have to explicitly specify the
 * desired field language; for example, $node->body['en'], thus overriding any
 * language negotiation rule that was previously applied.
 *
 * @see template_preprocess()
 * @see template_preprocess_node()
 * @see template_process()
 *
 * @ingroup themeable
 */
?>


<div id="node-<?php print $node->nid; ?>" class="<?php print $classes; ?> clearfix" <?php print $attributes; ?>>
  <div class="content" <?php print $content_attributes;?> >
    <?php
      // We hide the comments and links now so that we can render them later.
      hide($content['comments']);
      hide($content['links']);
    ?>
    <div class="aporta-box">
      <div class="imageAporta">
        <img title="<?php print $content['field_aporta_image'][0]['#item']['title'] ?>" alt="<?php print $content['field_aporta_image'][0]['#item']['alt'] ?>" src="<?php print file_create_url($content['field_aporta_image'][0]['#item']['uri']);
        ?>">
      </div>
      <div class="aporta-desafio-content">
        <div id="title">
          <?php  print $title; ?>
        </div>
        <div id="subtitle">
          <?php  print $content['field_aporta_subtitle'][0]['#markup']; ?>
        </div>
        <div id="contenidoDescripcion">
          <?php  print $content['body'][0]['#markup']; ?>
        </div>
      </div>
    </div>
    <div class="dge-actual-aporta-tabs" id="tabs">
      <ul>
      <?php if (isset($content['field_location'][0]['#markup'])  || isset($content['field_photo_place'][0]['#item']['uri']) || isset($content['field_location_gmaps'])
      || isset($content['field_place_description'][0]['#markup']) ): ?>
        <li><a href="#tabs-5" class="location"><span>Cuándo y dónde</span></a></li>
        <?php endif;?>
        <?php if (isset($content['field_content_inscriptions'][0]['#markup'])):?>
        <li><a href="#tabs-7" class="inscriptions"><span>Inscripciones</span></a></li>
        <?php endif;?>
        <?php if (isset($content['field_content_agenda'])):?>
        <li><a href="#tabs-1" class="calendar"><span>Agenda</span></a></li>
        <?php endif;?>
        <?php if (isset($content['field_description_ponents']) || isset($content['field_ponents_paragraph'])):?>
        <li><a href="#tabs-3" class="ponents"><span>Ponentes</span></a></li>
        <?php endif;?>
      </ul>
      <?php if (isset($content['field_location'][0]['#markup']) || isset($content['field_photo_place'][0]['#item']['uri']) || isset($content['field_location_gmaps'])
      || isset($content['field_place_description'][0]['#markup']) ): ?>
      <div id="tabs-5">
        <div class="dg-location">
          <?php
          print $content['field_location'][0]['#markup'];
          ?>
        </div>
        <div class="dg-date">
          <?php
          print str_replace('-',' de ',$content['field_aporta_date'][0]['#markup']);
          ?>
        </div>
        <div class="dg-box-left-location">
          <div class="dg-img">
            <img src="<?php print file_create_url($content['field_photo_place'][0]['#item']['uri'])?>">
            <?php if (isset($content['field_location_gmaps'])):?>
            <div id="localizacionImagenAporta"><img src="/sites/all/themes/dge_theme/images/svg/ping-map.svg" title="marker map" /><?php print ($content['field_location_gmaps']['#items'][0]['value']); ?></div>
            <?php endif;?>
          </div>
        </div>
        <div class="dg-box-right-location">
          <div class="dg-description">
            <?php
            print $content['field_place_description'][0]['#markup'];
            ?>
          </div>
        </div>
        <div class="dg-box-bottom-location">
          <div class="dg-mapa">
            <?php
            //print render($content['field_location_gmaps']);
             if (isset($content['field_direction_ign'])):?>
              <div id="localizacionImagenAporta" class="iconolocalizacion"><img src="/sites/all/themes/dge_theme/images/svg/ping-map.svg" title="marker map" style="" /><?php print ($content['field_direction_ign'][0]['#markup']);?></div>
              <?php endif;
            print render($content['field_address_current_aporta']);
            ?>
          </div>
        </div>
      </div>
      <?php endif;?>
      <?php if (isset($content['field_content_inscriptions'][0]['#markup'])):?>
      <div id="tabs-7">
        <div class="inscriptions">
          <?php
          print $content['field_content_inscriptions'][0]['#markup'];
          ?>
        </div>
      </div>
      <?php endif;?>
      <?php if (isset($content['field_content_agenda'])):?>
      <div id="tabs-1">
        <div class="agendaAporta">
          <?php
            print render($content['field_content_agenda']);
          ?>
        </div>
        <?php if (isset($content['field_group_aporta_doc'])):?>
        <div class="dge-detail__docs">
          <div class="dge-detail__docs-cont">
          Documentos
        </div>
        <div>
        <?php
          print render($content['field_group_aporta_doc']);
        ?></div>
        </div>
        <?php endif;?>
      </div>
      <?php endif;?>
      <?php if (isset($content['field_description_ponents']) || isset($content['field_ponents_paragraph'])):?>
      <div id="tabs-3">
        <div class="ponentsDescription">
          <?php
            print render($content['field_description_ponents']);
          ?>
        </div>
        <div class="ponents">
          <?php
          print render($content['field_ponents_paragraph']);
          ?>
        </div>
      </div>
      <?php endif;?>
    </div>
    <div class="contenidoRelacionadoAwards">
<?php print render($content['field_content_related']);?>
<?php print render($content['field_related_content']);?>

    </div>
  </div>
</div>
