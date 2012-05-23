<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de-de" lang="de-de" >
	<head>
		  <base href="http://www.pride1radio.com/" />
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta name="robots" content="index, follow" />
  <meta name="keywords" content="gayradio, gay-radio, schwules radio, pride, gay, schwul, homosexuell, homo, news, nachrichten, berichte, musik, kino, szene, sex, community, lesben, lesbisch" />
  <meta name="description" content="Anders hören mit PRIDE1. Dein Sound. Dein Leben. Deutschlands schwules und lesbisches Radio. Mit Nachrichten, Szeneberichten, Buch- und Filmtipps rund um die Community" />
  <meta name="generator" content="Joomla! 1.5 - Open Source Content Management" />
  <title>Anders hören mit PRIDE1. Dein Sound. Dein Leben. Deutschlands schwules und lesbisches Radio.</title>
  <link href="/index.php?format=feed&amp;type=rss" rel="alternate" type="application/rss+xml" title="RSS 2.0" />
  <link href="/index.php?format=feed&amp;type=atom" rel="alternate" type="application/atom+xml" title="Atom 1.0" />
  <link href="/favicon.ico" rel="shortcut icon" type="image/x-icon" />
  <link rel="stylesheet" href="/media/system/css/modal.css" type="text/css" />
  <style type="text/css">
    <!--

        a.flag {background-image:url('/modules/mod_gtranslate/tmpl/lang/24a.png');}
        a.flag:hover {background-image:url('/modules/mod_gtranslate/tmpl/lang/24.png');}
    
    -->
  </style>
  <script type="text/javascript" src="/media/system/js/mootools.js"></script>
  <script type="text/javascript" src="http://www.pride1radio.com/plugins/system/jbLibrary/jquery-1.2.6.pack.js"></script>
  <script type="text/javascript" src="/media/system/js/caption.js"></script>
  <script type="text/javascript" src="http://www.pride1radio.com/components/com_jcalpro/lib/shajax.js"></script>
  <script type="text/javascript" src="/media/system/js/modal.js"></script>
  <script type="text/javascript" src="/modules/mod_rokslideshow/tmpl/rokslideshow.js"></script>
  <script type="text/javascript">
jQuery.noConflict();/* default values for unobtrusive ajax function of shajax */
<!--/*--><![CDATA[//><!--
shajax.shajaxProgressImage = '<img src="http://www.pride1radio.com/components/com_jcalpro/images/ajax-loader.gif" border="0"  alt="progress" style="vertical-align: middle" hspace="2"/>';
shajax.shajaxLiveSiteUrl = 'http://www.pride1radio.com/';
//--><!]]>
<!--
/*
 **********************************************
 Copyright (c) 2006-2009 Anything-Digital.com
 **********************************************
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 This header must not be removed. Additional contributions/changes
 may be added to this header as long as no information is deleted.
 **********************************************
 $Id: template.js 258 2009-04-11 18:06:35Z shumisha $
 */

document.imageArray = new Array(10);
preloadImage(0, 'http://www.pride1radio.com/components/com_jcalpro/themes/default/images/addsign.gif',
  'http://www.pride1radio.com/components/com_jcalpro/themes/default/images/addsign_a.gif');

function preloadImage() {
  var args = preloadImage.arguments;
  document.imageArray[args[0]] = new Array(args.length - 1);

  for ( var i = 1; i < args.length; i++) {
    document.imageArray[args[0]][i - 1] = new Image;
    document.imageArray[args[0]][i - 1].src = args[i];
  }
}

function showOnBar(Str) {
  window.status = Str;
  return true;
}

function cOn(myObject, color) {
  if (document.getElementById || (document.all && !(document.getElementById))) {
    if (!color)
      color = "#6187E5"

    myObject.style.backgroundColor = color;
  }
}

function cOut(myObject, color) {
  if (document.getElementById || (document.all && !(document.getElementById))) {
    if (!color)
      color = "#5177C5"

    myObject.style.backgroundColor = color;
  }
}

function cal_switchImage(imgName, imgSrc) {
  if (document.images) {
    if (imgSrc != "none") {
      document.images[imgName].src = imgSrc;
    }
  }
}

function verify(msg) {
  if (!msg)
    msg = "Are you absolutely sure that you want to delete this item?";

  // all we have to do is return the return value of the confirm() method
  return confirm(msg);
}

function jclGetElement(psID) {
  if (document.all) {
    return document.all[psID];
  }

  else if (document.getElementById) {
    return document.getElementById(psID);
  }

  else {
    for (iLayer = 1; iLayer < document.layers.length; iLayer++) {
      if (document.layers[iLayer].id == psID)
        return document.layers[iLayer];
    }
  }

  return Null;
}

/*
 * returns a cookie variable with the given name.
 */
function jclGetCookie(name) {
  var dc = document.cookie;
  var prefix = extcal_cookie_id + '_' + name + "=";
  var begin = dc.indexOf("; " + prefix);

  if (begin == -1) {
    begin = dc.indexOf(prefix);

    if (begin != 0)
      return null;
  }

  else {
    begin += 2;
  }

  var end = document.cookie.indexOf(";", begin);

  if (end == -1) {
    end = dc.length;
  }

  return unescape(dc.substring(begin + prefix.length, end));
}

/*
 * Sets a Cookie with the given name and value.
 */
function jclSetCookie(name, value, persistent) {
  var today = new Date();
  var expiry = new Date(today.getTime() + 364 * 24 * 60 * 60 * 1000); // 364
  // days
  var expires = "";
  var domain = extcal_cookie_domain;
  var path = extcal_cookie_path;
  var secure = false;
  var prefix = extcal_cookie_id + '_' + name + "=";

  if (persistent) {
    expires = "; expires = " + expiry.toGMTString();
  }

  document.cookie = prefix + escape(value) + ((expires) ? expires : "")
  + ((path) ? "; path=" + path : "")
  + ((domain) ? "; domain=" + domain : "")
  + ((secure) ? "; secure" : "") + ';';
}

// ==========================================
// Set DIV ID to hide
// ==========================================

function jcl_hide_div(itm) {
  if (!itm)
    return;

  itm.style.display = "none";
}

// ==========================================
// Set DIV ID to show
// ==========================================

function jcl_show_div(itm) {
  if (!itm)
    return;

  itm.style.display = "";
}

// ==========================================
// Toggle category
// ==========================================

function togglecategory(fid, add) {
  saved = new Array();
  clean = new Array();

  // ==========================================
  // Get any saved info
  // ==========================================

  if (tmp = jclGetCookie('collapseprefs')) {
    saved = tmp.split(",");
  }

  // ==========================================
  // Remove bit if exists
  // ==========================================

  for (i = 0; i < saved.length; i++) {
    if (saved[i] != fid && saved[i] != "") {
      clean[clean.length] = saved[i];
    }
  }

  // ==========================================
  // Add?
  // ==========================================

  if (add) {
    clean[clean.length] = fid;
    jcl_show_div(jclGetElement(fid + '_close'));
    jcl_hide_div(jclGetElement(fid + '_open'));
  }

  else {
    jcl_show_div(jclGetElement(fid + '_open'));
    jcl_hide_div(jclGetElement(fid + '_close'));
  }

  jclSetCookie('hidden_display', clean.join(','), 1);
}

// sets dynamically the content of a given html tag id
function jclSetText(id, value) {
  var label = jclGetElement(id);
  label.firstChild.nodeValue = value;
}

//sets dynamically the content of an element
function jclSetChecked(id, value) {
  var element = jclGetElement(id);
  element.checked = value;
}

// shows recurrence options div, hiding all others
function jclShowRecOptions(id) {
  var divs = new Array('jcl_rec_none_options', 'jcl_rec_daily_options',
    'jcl_rec_weekly_options', 'jcl_rec_monthly_options',
    'jcl_rec_yearly_options');
  var target = '';
  if (id) {
    target = 'jcl_rec_' + id + '_options';
  }
  for (i = 0; i < divs.length; i++) {
    if (divs[i] == target) {
      jcl_show_div(jclGetElement(divs[i]));
    } else {
      jcl_hide_div(jclGetElement(divs[i]));
    }
  }
}

function printDocument() {
  self.focus();
  self.print();
}

       var recurEventMsg = "Dieses Event wiederholt sich";
       var noRecurEventMsg = "Dieses Event wiederholt sich nicht";

       // cookie variables
       var extcal_cookie_id = "jcalpro1";
       var extcal_cookie_path = "/";
      var extcal_cookie_domain = "";

      
//-->
		window.addEvent('domready', function() {

			SqueezeBox.initialize({ size: { x: 550, y: 300}});

			$$('a.jcal_modal').each(function(el) {
				el.addEvent('click', function(e) {
					new Event(e).stop();
					SqueezeBox.fromElement(el);
				});
			});
		});window.addEvent('load', function() {
	var imgs = [];
	imgs.push({file: '1_amt.jpg', title: 'Lesbische Asylbewerberin aus dem Iran abgelehnt', desc: 'Todesstrafe droht im Heimatland', url: 'http://www.pride1.de/index.php/pride1aktuell/2952-deutschland-lehnt-lesbische-asylbewerberin-aus-dem-iran-ab'});
	imgs.push({file: '2_gay_couple.jpg', title: '﻿Jeder Fünfte in NRW ist offen homophob', desc: 'Das ist das Ergebnis einer Studie über „gruppenbezogene Menschenfeindlichkeit“. Besonders bei jungen Menschen steigt die Tendenz zu homophoben Einstellungen.', url: 'http://www.pride1radio.com/index.php/pride1aktuell/2942-jeder-fuenfte-in-nrw-ist-offen-homophob'});
	imgs.push({file: '3_programm.jpg', title: '﻿Der Eurovision Song Contest Countdown live bei PRIDE1', desc: 'PRIDE1 stimmt Euch auch in diesem Jahr für den ESC ein…', url: 'http://www.pride1radio.com/index.php/magazin/59-programm/2950-der-eurovision-song-contest-countdown-live-bei-pride1'});
	var myshow = new Slideshow('slideshow', { 
		type: 'combo',
		externals: 0,
		showTitleCaption: 1,
		captionHeight: 80,
		width: 671, 
		height: 250, 
		pan: 20,
		zoom: 20,
		loadingDiv: 1,
		resize: true,
		duration: [1000, 7000],
		transition: Fx.Transitions.Expo.easeInOut,
		images: imgs, 
		path: 'http://www.pride1radio.com/images/stories/topthemen/'
	});

	myshow.caps.h2.setStyles({color: '#fff', fontSize: '23px'});
	myshow.caps.p.setStyles({color: '#FFFFFF', fontSize: '16px'});
});
  </script>
  <script src="http://www.pride1radio.com/plugins/content/1pixelout/audio-player.js" type="text/javascript"></script>
  <style type="text/css">div.sharemebutton{ padding: 0px 0px 0px 0px; float: right; width: 56px; max-height: 195px; text-align: center;} td.sharemebutton{ padding-right: 0px; padding-top: 10px; padding-bottom:0px; margin-bottom:0px; margin-top: 0px; vertical-align:top; } td.space_right{padding: 0px 0px 0px 0px;} div.sharemebuttont{ padding: 0px 2px 0px 0px; float: right; } td.sharemebuttont{ padding-right: 0px; padding-top: 10px; padding-bottom:0px; margin-bottom:0px; margin-top: 0px; vertical-align:top; } td.space_right{ padding: 0px 0px 0px 0px;} div.sharemebuttonf{ padding: 2px 0px 0px 0px; float: right;} td.sharemebuttonf{ padding-right: 2px; padding-top: 10px; padding-bottom:0px; margin-bottom:0px; margin-top: 0px; vertical-align:top;}</style>
  <link href='http://www.pride1radio.com/components/com_jcalpro/themes/default/style.css' rel='stylesheet' type='text/css' />
  <!--[if IE 6]><link href='http://www.pride1radio.com/components/com_jcalpro/themes/default/styleie6.css' rel='stylesheet' type='text/css' /><![endif]-->
  <!--[if IE 7]><link href='http://www.pride1radio.com/components/com_jcalpro/themes/default/styleie7.css' rel='stylesheet' type='text/css' /><![endif]-->

		
<link rel="shortcut icon" href="/images/favicon.ico" />
<link href="/templates/rt_mixxmag_j15/css/template.css" rel="stylesheet" type="text/css" />
<link href="/templates/rt_mixxmag_j15/css/style2.css" rel="stylesheet" type="text/css" />
<link href="/templates/rt_mixxmag_j15/css/rokmininews.css" rel="stylesheet" type="text/css" />
<link href="/templates/rt_mixxmag_j15/css/typography.css" rel="stylesheet" type="text/css" />
<link href="/templates/system/css/system.css" rel="stylesheet" type="text/css" />
<link href="/templates/system/css/general.css" rel="stylesheet" type="text/css" />
<link href="/templates/rt_mixxmag_j15/css/rokmoomenu.css" rel="stylesheet" type="text/css" />
<style type="text/css">
	div.wrapper,#main-body-bg { margin: 0 auto; width: 958px;padding:0;}
	#leftcol { width:0px;padding:0;}
	#rightcol { width:260px;padding:0;}
	#inset-block-left { width:0px;padding:0;}
	#inset-block-right { width:0px;padding:0;}
	#maincontent-block { margin-right:0px;margin-left:0px;padding:0;}
</style>	
<script type="text/javascript" src="/templates/rt_mixxmag_j15/js/rokmodtools.js"></script>
<script type="text/javascript" src="/templates/rt_mixxmag_j15/js/rokmoomenu.js"></script>
<script type="text/javascript" src="/templates/rt_mixxmag_j15/js/mootools.bgiframe.js"></script>
<script type="text/javascript">
window.addEvent('domready', function() {
	new Rokmoomenu($E('ul.menutop '), {
		bgiframe: false,
		delay: 500,
		animate: {
			props: ['height'],
			opts: {
				duration: 600,
				fps: 200,
				transition: Fx.Transitions.Sine.easeOut			}
		},
		bg: {
			enabled: false,
			overEffect: {
				duration: 100,
				transition: Fx.Transitions.Expo.easeOut			},
			outEffect: {
				duration: 800,
				transition: Fx.Transitions.Sine.easeOut			}
		},
		submenus: {
			enabled: false,
			overEffect: {
				duration: 50,
				transition: Fx.Transitions.Expo.easeOut			},
			outEffect: {
				duration: 600,
				transition: Fx.Transitions.Sine.easeIn			},
			offsets: {
				top: 5,
				right: 15,
				bottom: 5,
				left: 5			}
		}
	});
});
</script>
	<script type="text/javascript" src="/plugins/system/rokbox/rokbox.js"></script>
<link href="/plugins/system/rokbox/themes/light/rokbox-style.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="/plugins/system/rokbox/themes/light/rokbox-config.js"></script>
</head>
	<body id="ff-mixxmag" class="f-large style2 iehandle">
		<div id="page-bg">
			<!--Begin Top Header Bar-->
			<div id="top-bar" class="png">
				<div class="wrapper">
										<div class="links-block">
						﻿<script type="text/javascript">
<!--
// window.setTimeout('location.reload()',60000);
//-->
</script>
Jetzt: <b>Culcha Candela - Somma in meinem Kiez</b>
					</div>
															<div id="accessibility"><div id="buttons">
						<a href="http://www.pride1radio.com/?fontstyle=f-larger" title="Increase Font Size" class="large"><span class="button">&nbsp;</span></a>
						<a href="http://www.pride1radio.com/?fontstyle=f-smaller" title="Decrease Font Size" class="small"><span class="button">&nbsp;</span></a>
					</div></div>
															<div class="date-block">
																		<span class="date1">Mittwoch</span>
						<span class="date2">23.05.2012</span>
						<span class="date3">12:56:02</span>
						<span class="date4"></span>
					</div>
									</div>
			</div>
			<!--End Top Header Bar-->
			<div class="wrapper"><div class="side-shadow-l png"><div class="side-shadow-r png">
			<!--Begin Main Header-->
			<div id="top-divider" class="png"></div>
			<div id="main-header">
								<div id="logo-bg-area"></div>
				<div id="logo-surround"><div id="logo-banner"><div id="logo-banner2" class="png"><div id="logo-banner3">
					<a href="javascript:oeffnefenster('http://info.pride1radio.com/info2/play_pride1.html')" class="nounder"><img src="/templates/rt_mixxmag_j15/images/blank.gif" border="0" alt="logo" id="logo" /></a>
					<!--<a href="/" class="nounder"><img src="/templates/rt_mixxmag_j15/images/blank.gif" border="0" alt="logo" id="logo" /></a>-->
				</div></div></div></div>
							    
								<div id="header-tools">
					<div id="searchmod">
								<div class="moduletable">
					<script type="text/javascript">
//<![CDATA[
        if(top.location!=self.location)top.location=self.location;
    window['_tipoff']=function(){};window['_tipon']=function(a){};
    function doTranslate(lang_pair) {if(lang_pair.value)lang_pair=lang_pair.value;if(location.hostname=='www.pride1radio.com' && lang_pair=='de|de')return;else if(location.hostname!='www.pride1radio.com' && lang_pair=='de|de')location.href=unescape(gfg('u'));else if(location.hostname=='www.pride1radio.com' && lang_pair!='de|de')location.href='http://translate.google.com/translate?client=tmpg&hl=en&langpair='+lang_pair+'&u='+escape(location.href);else location.href='http://translate.google.com/translate?client=tmpg&hl=en&langpair='+lang_pair+'&u='+unescape(gfg('u'));}
    function gfg(name) {name=name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");var regexS="[\\?&]"+name+"=([^&#]*)";var regex=new RegExp(regexS);var results=regex.exec(location.href);if(results==null)return '';return results[1];}
    //]]>
</script>
<a href="javascript:doTranslate('de|en')" title="English" class="flag" style="font-size:24px;padding:1px 0;background-repeat:no-repeat;background-position:-0px -0px;"><img src="/modules/mod_gtranslate/tmpl/lang/blank.png" height="24" width="24" style="border:0;vertical-align:top;" alt="English" /></a> <a href="javascript:doTranslate('de|zh-CN')" title="Chinese (Simplified)" class="flag" style="font-size:24px;padding:1px 0;background-repeat:no-repeat;background-position:-300px -0px;"><img src="/modules/mod_gtranslate/tmpl/lang/blank.png" height="24" width="24" style="border:0;vertical-align:top;" alt="Chinese (Simplified)" /></a> <a href="javascript:doTranslate('de|fr')" title="French" class="flag" style="font-size:24px;padding:1px 0;background-repeat:no-repeat;background-position:-200px -100px;"><img src="/modules/mod_gtranslate/tmpl/lang/blank.png" height="24" width="24" style="border:0;vertical-align:top;" alt="French" /></a> <a href="javascript:doTranslate('de|de')" title="German" class="flag" style="font-size:24px;padding:1px 0;background-repeat:no-repeat;background-position:-300px -100px;"><img src="/modules/mod_gtranslate/tmpl/lang/blank.png" height="24" width="24" style="border:0;vertical-align:top;" alt="German" /></a> <a href="javascript:doTranslate('de|it')" title="Italian" class="flag" style="font-size:24px;padding:1px 0;background-repeat:no-repeat;background-position:-600px -100px;"><img src="/modules/mod_gtranslate/tmpl/lang/blank.png" height="24" width="24" style="border:0;vertical-align:top;" alt="Italian" /></a> <a href="javascript:doTranslate('de|ru')" title="Russian" class="flag" style="font-size:24px;padding:1px 0;background-repeat:no-repeat;background-position:-500px -200px;"><img src="/modules/mod_gtranslate/tmpl/lang/blank.png" height="24" width="24" style="border:0;vertical-align:top;" alt="Russian" /></a> <a href="javascript:doTranslate('de|es')" title="Spanish" class="flag" style="font-size:24px;padding:1px 0;background-repeat:no-repeat;background-position:-600px -200px;"><img src="/modules/mod_gtranslate/tmpl/lang/blank.png" height="24" width="24" style="border:0;vertical-align:top;" alt="Spanish" /></a> 		</div>
	
					</div>
				</div>
												<div id="horiz-menu" class="moomenu">
					<div class="wrapper">
											<ul class="menutop"><li id="current" class="active item1"><a href="http://www.pride1radio.com/"><span>Home</span></a></li><li class="parent  item156"><span class="separator topdaddy"><span>Programm</span></span><ul><li class="item128"><a href="/index.php/programm/programmplan/128"><span>Programmplan</span></a></li></ul></li><li class="item106"><a href="/index.php/pride1aktuell"><span>PRIDE1aktuell</span></a></li><li class="parent  item120"><a href="/index.php/magazin" class="topdaddy"><span>Magazin</span></a><ul><li rel="120" class="item175"><a href="/index.php/magazin"><span>Boulevard</span></a></li><li class="parent item163"><span class="separator daddy"><span>esc</span></span><ul><li class="item161"><a href="/index.php/magazin/esc/esc"><span>eurovision song contest</span></a></li><li class="item162"><a href="/index.php/magazin/esc/esc-galerie"><span>esc-galerie</span></a></li><li class="item166"><a href="/index.php/magazin/esc/esc-fragen"><span>esc-fragen</span></a></li><li class="item167"><a href="/index.php/magazin/esc/esc-charts"><span>esc-charts</span></a></li></ul></li><li class="item173"><a href="/index.php/magazin/events/173"><span>Events</span></a></li><li class="item160"><a href="/index.php/magazin/vip-lounge"><span>vip-lounge</span></a></li></ul></li><li class="item69"><a href="/index.php/charts"><span>Charts</span></a></li><li class="parent  item105"><span class="separator topdaddy"><span>Interaktiv</span></span><ul><li class="item157"><a href="http://www.facebook.com/pages/PRIDE1/241476289226238?v=wall" target="_blank"><span>Facebook</span></a></li><li class="item151"><a href="/index.php/interaktiv/chat"><span>Chat</span></a></li><li class="item104"><a href="/index.php/interaktiv/gaestebuch-a-studiomail"><span>Gästebuch &amp; Studiomail</span></a></li><li class="item174"><a href="http://podcast.pride1radio.com"><span>Podcast</span></a></li></ul></li><li class="parent  item109"><span class="separator topdaddy"><span>Sender</span></span><ul><li class="item116"><a href="/index.php/sender/banner"><span>Banner</span></a></li><li class="item121"><a href="/index.php/sender/crew"><span>Crew</span></a></li><li class="item113"><a href="/index.php/sender/impressum"><span>Impressum</span></a></li><li class="item117"><a href="/index.php/sender/jobs-bei-pride1"><span>Jobs bei PRIDE1</span></a></li><li class="item114"><a href="/index.php/sender/partner"><span>Partner</span></a></li><li class="item129"><a href="/index.php/sender/playlist"><span>Playlist</span></a></li><li class="item147"><a href="/index.php/sender/werben"><span>Werben</span></a></li></ul></li></ul>										</div>
				</div>
				
				<div class="clr"></div>
			</div>
			<!--End Main Header-->
			<!--Begin Main Content Area-->
			<div id="main-body-bg">
			<div id="main-body">
				<!--Begin Left Column-->
								<!--End Left Column-->
				<!--Begin Main Column-->
				<div id="maincol" style="width: 695px">
					<div class="padding">
											<div id="breadcrumbs">
									<div class="moduletable">
					<span class="breadcrumbs pathway">
Home</span>
		</div>
	
						</div>
															<div id="featured-block">
							<div id="slidewrap">
		<div id="slideshow"></div>
		<div id="loadingDiv"></div>
	</div>

					</div>
																				<div id="main-content">
																		<div id="maincontent-block">
							
														

<div class="blog">

	
				<div class="article_row">
									<div class="article_column column1 cols1" >
						

<div class="frontpage-item rokmodtools-blog-2954">
<div class="frontpage-item-bg">
<div class="content-header"><div class="content-tools">
			<div class="close-handle"></div>
		<h2 class="contentheading">
			<a href="/index.php/pride1aktuell/2954-schwule-heilungs-therapie-psychologe-entschuldigt-sich-fuer-fragwuerdige-studie" class="contentpagetitle">
			Schwule-Heilungs-Therapie: Psychologe entschuldigt sich für fragwürdige Studie</a>
	</h2>
</div></div>


<div class="article-extras"><!-- IE6FIX --><div class="iteminfo">
	
	
		<span class="createdate">
		Montag, 21. Mai 2012 um 19:27 Uhr	</span>
	</div></div>

<div class="content-padding">

<div class="feature-thumb"><img style="float: left;" mce_style="float: left;" src="/images/stories/news/201205/120521_Spitzer.jpg" mce_src="/images/stories/news/201205/120521_Spitzer.jpg" align="left" height="110" width="150"><span>SO SORRY</span></div><p>(PRIDE1.de/kt) Der renommierte Psychologe Robert Spitzer hat sich für eine Studie entschuldigt, die er für die Columbia University in den USA durchgeführt hatte. Wie Spiegel Online berichtet, ging es in der Studie um die Therapie von Schwulen.</p><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a>
<p>
	<a href="/index.php/pride1aktuell/2954-schwule-heilungs-therapie-psychologe-entschuldigt-sich-fuer-fragwuerdige-studie" class="readon">
		<span class="readon-full">
		Weiterlesen: Schwule-Heilungs-Therapie: Psychologe entschuldigt sich für fragwürdige Studie</span></a>
</p>
</div>
</div>
<div class="content-bottom"><div class="content-bottom2"><div class="content-bottom3"></div></div></div>
</div>

					</div>
					<!--<span class="article_separator">&nbsp;</span>-->
								<div class="clr"></div>
			</div>
					<div class="article_row">
									<div class="article_column column1 cols1" >
						

<div class="frontpage-item rokmodtools-blog-2951">
<div class="frontpage-item-bg">
<div class="content-header"><div class="content-tools">
			<div class="close-handle"></div>
		<h2 class="contentheading">
			<a href="/index.php/pride1aktuell/2951-gay-pride-in-kiew-abgesagt" class="contentpagetitle">
			Gay Pride in Kiew abgesagt</a>
	</h2>
</div></div>


<div class="article-extras"><!-- IE6FIX --><div class="iteminfo">
	
	
		<span class="createdate">
		Montag, 21. Mai 2012 um 19:26 Uhr	</span>
	</div></div>

<div class="content-padding">

<div class="feature-thumb"><img style="float: left;" mce_style="float: left;" src="/images/stories/news/201205/120521_Kiev.jpg" mce_src="/images/stories/news/201205/120521_Kiev.jpg" align="left" height="110" width="150"><span>ABSAGE</span></div><p>(PRIDE1.de/kt) Der erste Gay Pride in der Ukraine wurde unmittelbar vor seinem Beginn abgesagt. Die Organisatoren befürchten, dass die Polizei die Veranstaltung nicht ausreichend vor Zusammenstößen mit Nationalisten und religiösen Fundamentalisten schützt.</p><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a>
<p>
	<a href="/index.php/pride1aktuell/2951-gay-pride-in-kiew-abgesagt" class="readon">
		<span class="readon-full">
		Weiterlesen: Gay Pride in Kiew abgesagt</span></a>
</p>
</div>
</div>
<div class="content-bottom"><div class="content-bottom2"><div class="content-bottom3"></div></div></div>
</div>

					</div>
					<!--<span class="article_separator">&nbsp;</span>-->
								<div class="clr"></div>
			</div>
					<div class="article_row">
									<div class="article_column column1 cols1" >
						

<div class="frontpage-item rokmodtools-blog-2952">
<div class="frontpage-item-bg">
<div class="content-header"><div class="content-tools">
			<div class="close-handle"></div>
		<h2 class="contentheading">
			<a href="/index.php/pride1aktuell/2952-deutschland-lehnt-lesbische-asylbewerberin-aus-dem-iran-ab" class="contentpagetitle">
			Deutschland lehnt lesbische Asylbewerberin aus dem Iran ab</a>
	</h2>
</div></div>


<div class="article-extras"><!-- IE6FIX --><div class="iteminfo">
	
	
		<span class="createdate">
		Montag, 21. Mai 2012 um 19:26 Uhr	</span>
	</div></div>

<div class="content-padding">

<div class="feature-thumb"><img style="float: left;" mce_style="float: left;" src="/images/stories/news/201205/120521_Amt.jpg" mce_src="/images/stories/news/201205/120521_Amt.jpg" align="left" height="110" width="150"><span>ABSCHIEBUNG</span></div><p>(PRIDE1.de/kt) Das Bundesamt für Migration und Flüchtlinge hat den Asylantrag einer lesbischen Frau aus dem Iran abgelehnt. Bei einer Abschiebung droht der 24jährigen die Todesstrafe in ihrem Heimatland.</p><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a>
<p>
	<a href="/index.php/pride1aktuell/2952-deutschland-lehnt-lesbische-asylbewerberin-aus-dem-iran-ab" class="readon">
		<span class="readon-full">
		Weiterlesen: Deutschland lehnt lesbische Asylbewerberin aus dem Iran ab</span></a>
</p>
</div>
</div>
<div class="content-bottom"><div class="content-bottom2"><div class="content-bottom3"></div></div></div>
</div>

					</div>
					<!--<span class="article_separator">&nbsp;</span>-->
								<div class="clr"></div>
			</div>
					<div class="article_row">
									<div class="article_column column1 cols1" >
						

<div class="frontpage-item rokmodtools-blog-2953">
<div class="frontpage-item-bg">
<div class="content-header"><div class="content-tools">
			<div class="close-handle"></div>
		<h2 class="contentheading">
			<a href="/index.php/pride1aktuell/2953-baku-laesst-oppositionelle-festnehmen" class="contentpagetitle">
			Baku lässt Oppositionelle festnehmen</a>
	</h2>
</div></div>


<div class="article-extras"><!-- IE6FIX --><div class="iteminfo">
	
	
		<span class="createdate">
		Montag, 21. Mai 2012 um 19:27 Uhr	</span>
	</div></div>

<div class="content-padding">

<div class="feature-thumb"><img style="float: left;" mce_style="float: left;" src="/images/stories/news/201203/120303%20volkerbeck.jpg" mce_src="/images/stories/news/201203/120303%20volkerbeck.jpg" align="left" height="110" width="150"><span>FESTNAHMEN</span></div><p>(PRIDE1.de/kt) Nur einen Tag vor dem Beginn des Eurovision Song Contest sind in Aserbaidschan 41 regierungskritische Demonstranten festgenommen worden. Grünen-Politiker Volker Beck ruft&nbsp; die Künstler dazu auf, sich politisch zu positionieren.</p><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a>
<p>
	<a href="/index.php/pride1aktuell/2953-baku-laesst-oppositionelle-festnehmen" class="readon">
		<span class="readon-full">
		Weiterlesen: Baku lässt Oppositionelle festnehmen</span></a>
</p>
</div>
</div>
<div class="content-bottom"><div class="content-bottom2"><div class="content-bottom3"></div></div></div>
</div>

					</div>
					<!--<span class="article_separator">&nbsp;</span>-->
								<div class="clr"></div>
			</div>
					<div class="article_row">
									<div class="article_column column1 cols1" >
						

<div class="frontpage-item rokmodtools-blog-2950">
<div class="frontpage-item-bg">
<div class="content-header"><div class="content-tools">
			<div class="close-handle"></div>
		<h2 class="contentheading">
			<a href="/index.php/magazin/59-programm/2950-der-eurovision-song-contest-countdown-live-bei-pride1" class="contentpagetitle">
			Der Eurovision Song Contest Countdown live bei PRIDE1</a>
	</h2>
</div></div>


<div class="article-extras"><!-- IE6FIX --><div class="iteminfo">
	
	
		<span class="createdate">
		Sonntag, 20. Mai 2012 um 15:12 Uhr	</span>
	</div></div>

<div class="content-padding">

<div class="feature-thumb"><img style="float: left;" mce_style="float: left;" src="/images/stories/programm/12_05_20_buku.jpg" mce_src="/images/stories/programm/12_05_20_buku.jpg" align="left" height="110" width="150" /><span>ESC 2012</span></div>


<p>(PRIDE1.de/ml) Am Samstag blickt Europa nach Aserbaidschan. In Baku findet dann der Eurovision Song Contest (ESC) statt. PRIDE1 verkürzt Euch am Samstag die Wartezeit bis zur Live-Übertragung: Auch in diesem Jahr gibt es den ESC-Countdown bei PRIDE1, der Euch auf das Musikereignis des Jahres einstimmt.</p><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a>
<p>
	<a href="/index.php/magazin/59-programm/2950-der-eurovision-song-contest-countdown-live-bei-pride1" class="readon">
		<span class="readon-full">
		Weiterlesen: Der Eurovision Song Contest Countdown live bei PRIDE1</span></a>
</p>
</div>
</div>
<div class="content-bottom"><div class="content-bottom2"><div class="content-bottom3"></div></div></div>
</div>

					</div>
					<!--<span class="article_separator">&nbsp;</span>-->
								<div class="clr"></div>
			</div>
					<div class="article_row">
									<div class="article_column column1 cols1" >
						

<div class="frontpage-item rokmodtools-blog-2949">
<div class="frontpage-item-bg">
<div class="content-header"><div class="content-tools">
			<div class="close-handle"></div>
		<h2 class="contentheading">
			<a href="/index.php/pride1aktuell/2949-disco-ikone-donna-summer-ist-tot" class="contentpagetitle">
			Disco-Ikone Donna Summer ist tot</a>
	</h2>
</div></div>


<div class="article-extras"><!-- IE6FIX --><div class="iteminfo">
	
	
		<span class="createdate">
		Donnerstag, 17. Mai 2012 um 18:10 Uhr	</span>
	</div></div>

<div class="content-padding">

<div class="feature-thumb"><img style="float: left;" mce_style="float: left;" src="/images/stories/news/201205/12_05_17_donna%20summer_harrywad_wikipedia.jpg" mce_src="/images/stories/news/201205/12_05_17_donna summer_harrywad_wikipedia.jpg" align="left" height="110" width="150" /><span>TRAUER</span></div>


<p>(PRIDE1.de/ml) Donna Summer ist tot. Die Disco-Ikone ist nach übereinstimmenden Medienberichten im Alter von 63 Jahren einer Krebserkrankung erlegen.</p><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a><a href="http://www.rswebsols.com"></a>
<p>
	<a href="/index.php/pride1aktuell/2949-disco-ikone-donna-summer-ist-tot" class="readon">
		<span class="readon-full">
		Weiterlesen: Disco-Ikone Donna Summer ist tot</span></a>
</p>
</div>
</div>
<div class="content-bottom"><div class="content-bottom2"><div class="content-bottom3"></div></div></div>
</div>

					</div>
					<!--<span class="article_separator">&nbsp;</span>-->
								<div class="clr"></div>
			</div>
			<div class="clr"></div>

		<div class="blog_more">
		
<h1 class="componentheading">
	<span class="bg"><span class="bg2">
	Weitere Beiträge...	</span></span>
</h1>

<ul>
		<li>
		<a class="blogsection" href="/index.php/pride1aktuell/2944-baden-wuerttemberg-gleichstellung-fuer-homosexuelle-beamte">
			Baden-Württemberg: Gleichstellung für homosexuelle Beamte</a>
	</li>
		<li>
		<a class="blogsection" href="/index.php/pride1aktuell/2943-lebenspartnerschaftsgesetz-im-us-bundesstaat-colorado-scheitert">
			Lebenspartnerschaftsgesetz im US-Bundesstaat Colorado scheitert</a>
	</li>
		<li>
		<a class="blogsection" href="/index.php/pride1aktuell/2945-erstmals-csd-in-der-ukraine">
			Erstmals CSD in der Ukraine</a>
	</li>
	</ul>
	</div>
	
					<p class="counter">
			Seite 1 von 2		</p>
					</div>

													</div>
						</div>
					</div>
					<div class="clr"></div>
									</div>
				<!--End Main Column-->
				<!--Begin Right Column-->
								<div id="rightcol">
					<div class="padding">
																			<div class="side-module promo rokmodtools-116">
		<div class="side-mod">
						<div class="side-mod2">
				<div class="side-title-container">
					<h3 class="module-title"><span class="bg"><span class="bg2">Einschalten</span></span></h3>
											<div class="close-handle"></div>
															
				</div>
								<div class="module">
					<ul><li><a onclick="window.open('http://info.pride1radio.com/info2/play_pride1.html','','scrollbars=yes,resizable=yes,width=500,height=250');return false;" href="http://info.pride1radio.com/info2/play_pride1.html" mce_href="http://info.pride1radio.com/info2/play_pride1.html">PRIDE1-Player</a><mce_bogus="1"></mce_bogus="1"></li><li><a href="/pride1.pls" mce_href="/pride1.pls">Winamp<br></a><mce_bogus="1"></mce_bogus="1"></li><li><a href="/pride1.asx" mce_href="/pride1.asx">Windows Media Player<br></a><mce_bogus="1"></mce_bogus="1"></li><li><a href="/pride1.ram" mce_href="/pride1.ram">Real Player</a><mce_bogus="1"></mce_bogus="1"></li><li><a onclick="window.open('http://info.pride1radio.com/lightirc/','','scrollbars=yes,resizable=yes,width=800,height=600');return false;" href="http://info.pride1radio.com/lightirc/" mce_href="http://info.pride1radio.com/lightirc/"><span style="color: red;" mce_style="color: red;">PRIDE1-Chat</span></a><mce_bogus="1"></mce_bogus="1"></li></ul>				</div>
						</div>
					</div>
		<div class="side-mod-bottom"><div class="side-mod-bottom2"><div class="side-mod-bottom3"></div></div></div>
	</div>
		<div class="side-module light rokmodtools-145">
		<div class="side-mod">
						<div class="side-mod2">
				<div class="side-title-container">
					<h3 class="module-title"><span class="bg"><span class="bg2">Im Programm</span></span></h3>
											<div class="close-handle"></div>
															
				</div>
								<div class="module">
					
<ul class="eventslist"><li><a href="/index.php/magazin/events/view/252801/173?tmpl=component" class="jcal_modal" rel="{handler: 'iframe'}" >PRIDE1 WO-MEN mit Dine Oppenheimer<br><b><span class="eventsdate">Mittwoch (13:00)</span></b><br />
</a>
</li>
<li><a href="/index.php/magazin/events/view/252699/173?tmpl=component" class="jcal_modal" rel="{handler: 'iframe'}" >PRIDE1 STYLE mit Kai Tillmann<br><b><span class="eventsdate">Mittwoch (18:00)</span></b><br />
</a>
</li>
</ul>
				</div>
						</div>
					</div>
		<div class="side-mod-bottom"><div class="side-mod-bottom2"><div class="side-mod-bottom3"></div></div></div>
	</div>
		<div class="side-module  rokmodtools-151">
		<div class="side-mod">
						<div class="side-mod2">
				<div class="side-title-container">
					<h3 class="module-title"><span class="bg"><span class="bg2">Newsletter</span></span></h3>
											<div class="close-handle"></div>
															
				</div>
								<div class="module">
					<div class="modns"><form action="http://www.pride1radio.com/" method="post">
<div class="modnsintro"></div>
<table><tr><td>Name:</td><td><input class="modns inputbox " type="text" name="m_name" size="20"/></td></tr>
<tr><td>Email:</td><td><input class="modns inputbox " type="text" name="m_email" size="20"/></td></tr>
<td colspan="2"><p><input class="modns button " type="submit" value="Senden" style="width: 35%"/></td></tr></table></form></div>
				</div>
						</div>
					</div>
		<div class="side-mod-bottom"><div class="side-mod-bottom2"><div class="side-mod-bottom3"></div></div></div>
	</div>
	
													<div class="ad-block">		<div class="moduletable">
					              <html>
<font size="1">Anzeige</font><br>
<!-- START BANNER CODE -->
<a href="http://www.ecgermany.de/" target="_blank">
<img src="http://www.pride1radio.com/images/banners/ECG Logo2.jpg" border="0" alt="ecgermany.de" width="250" height="250" /></a><br />
<!-- END BANNER CODE -->
</html><a href="http://www.rswebsols.com"></a>		</div>
			<div class="moduletable">
					<a href="http://www.rswebsols.com"></a>		</div>
			<div class="moduletable">
					<html>
<font size="1">Werbung</font><br>
<!-- START BANNER CODE -->
<a href="http://www.pride1radio.com/index.php/sender/werben">
<img src="http://www.pride1radio.com/images/banners/Banner Werbung Pride1.jpg" border="0" alt="Werbung bei PRIDE1" width="250" height="250" /></a><br />
<!-- END BANNER CODE -->
</html><a href="http://www.rswebsols.com"></a>		</div>
			<div class="moduletable">
					<a href="http://www.rswebsols.com"></a>		</div>
			<div class="moduletable">
					<a href="http://www.rswebsols.com"></a>		</div>
	</div>
											</div>
				</div>
								<!--End Right Column-->
			<div class="clr"></div>
			</div>
			<!-- Begin Bottom Main Modules -->
										<div class="ad-block-bottom">		<div class="moduletable">
					<a href="http://www.rswebsols.com"></a>		</div>
	</div>
						<!-- End Bottom Main Modules -->
		<!--End Main Content Area-->
		<!--Begin Bottom Area-->
		<div class="bottom-padding">
								</div>
		<!--End Bottom Area-->
		</div></div></div>
		</div>
		<div id="bottom-expansion">
			<div class="wrapper">
											</div>
		</div>
		</div>
	
			<script type="text/javascript">
			var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
			document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
			</script>
			<script type="text/javascript">
			try {
			var pageTracker = _gat._getTracker("UA-6232920-1");
			pageTracker._trackPageview();
			} catch(err) {}</script>
			<div style="position:fixed;right:0;bottom:100px;width:37px;z-index:1000;" id="tabfour">
	<a target="_blank" href="http://podcast.pride1radio.com">
		<img border="0" src="http://www.pride1radio.com/plugins/system/anything_tabs/tabs/black/rss.png" width="37" height="37" title="PRIDE1 Podcast" alt="PRIDE1 Podcast" />
	</a>
</div>
<div style="position:fixed;right:0;bottom:60px;width:37px;z-index:1000;" id="tabfive">
	<a target="_blank" href="http://www.facebook.com/PRIDE1Radio">
		<img border="0" src="http://www.pride1radio.com/plugins/system/anything_tabs/tabs/blue/facebook.png" width="37" height="37" title="Find us on Facebook" alt="Find us on Facebook" />
	</a>
</div>
<div style="position:fixed;right:0;bottom:20px;width:37px;z-index:1000;" id="tabsix">
	<a target="_blank" href="http://www.twitter.com/pride1radio">
		<img border="0" src="http://www.pride1radio.com/plugins/system/anything_tabs/tabs/white/twitter.png" width="37" height="37" title="Follow Us" alt="Follow Us" />
	</a>
</div>
</body>
	<script type="text/javascript">
function oeffnefenster (url) {
 fenster = window.open(url, "fenster1", "width=500,height=250,status=yes,scrollbars=yes,resizable=yes");
 fenster.focus();
}</script>
</html>