<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="../../shared/commontemplates.xsl"/>

    <!-- Handle the portlet for the Google.org search -->
    <xsl:template match="portlets[/response/view/@type='gsa']">
        <div id="right" class="box1 homeRightPortlets">
            <xsl:for-each select="portlet[@type='googlecomresults']">
                <div class="box2">
                    <div class="header">
                        <div class="headerContainer">
                            <h1>
                                <a href="http://www.google.com/search?q={/response/GSP/Q}"><img src="{$staticprefix}images/google_logo_25wht.gif" border="0"
                                    style="vertical-align:middle"
                                    alt="Google Search>"/> Search Results</a>
                            </h1>
                        </div>
                    </div>
                    <div class="content" id="newWorkspaces">
                        <ul class="listgoogle">
                            <xsl:for-each select="result">
                                <li>
                                    <a href="{url}">
                                        <xsl:value-of disable-output-escaping="yes" select="title"/>
                                    </a>
                                    <p><xsl:value-of disable-output-escaping="yes" select="context"/></p>
                                </li>
                            </xsl:for-each>
                        </ul>
                    </div>
                    <div style="text-align:center; font-family:Verdana, Arial, Helvetica, sans-serif; font-size:11px">
                        <span>...search</span> <a href="http://www.google.com/search?q={/response/GSP/Q}">
                            <img src="{$staticprefix}images/google_logo_25wht.gif" border="0"
                                style="vertical-align:middle"
                                alt="Google Search>"/>
                        </a>
                    </div>
                </div>
            </xsl:for-each>
        </div>
    </xsl:template>

    <xsl:template match="view[@name='gsa.html' and @type='gsa']">
        <xsl:apply-templates select="../GSP"/>
    </xsl:template>

    <!-- *** onebox information *** -->
    <xsl:variable name="show_onebox">1</xsl:variable>

    <!-- *** db_url_protocol: googledb:// *** -->
    <xsl:variable name="db_url_protocol">googledb://</xsl:variable>

    <!-- *** analytics information *** -->
    <xsl:variable name="analytics_account"/>
    <xsl:variable name="show_top_navigation">1</xsl:variable>

    <xsl:variable name="choose_bottom_navigation">1</xsl:variable>
    <!-- *** sort by date/relevance *** -->
    <xsl:variable name="show_sort_by">1</xsl:variable>
    <!-- *** analytics_script_url: http://www.google-analytics.com/urchin.js *** -->
    <xsl:variable name="analytics_script_url">http://www.google-analytics.com/urchin.js</xsl:variable>

    <!-- **********************************************************************
        Logo setup (can be customized)
        - whether to show logo: 0 for FALSE, 1 (or non-zero) for TRUE
        - logo url
        - logo size: '' for default image size
        ********************************************************************** -->
    <xsl:variable name="show_logo">1</xsl:variable>
    <xsl:variable name="logo_url">images/Title_Left.gif</xsl:variable>
    <xsl:variable name="logo_width">200</xsl:variable>
    <xsl:variable name="logo_height">78</xsl:variable>

    <!-- *** spelling suggestions *** -->
    <xsl:variable name="show_spelling">1</xsl:variable>
    <xsl:variable name="spelling_text">Did you mean:</xsl:variable>
    <xsl:variable name="spelling_text_color">#cc0000</xsl:variable>

    <!-- *** synonyms suggestions *** -->
    <xsl:variable name="show_synonyms">1</xsl:variable>
    <xsl:variable name="synonyms_text">You could also try:</xsl:variable>
    <xsl:variable name="synonyms_text_color">#cc0000</xsl:variable>

    <!-- *** search boxes *** -->
    <xsl:variable name="show_top_search_box">1</xsl:variable>
    <xsl:variable name="show_bottom_search_box">0</xsl:variable>

    <!-- *** choose separation bar: 'ltblue', 'blue', 'line', 'nothing' *** -->
    <xsl:variable name="choose_sep_bar">ltblue</xsl:variable>
    <xsl:variable name="sep_bar_std_text">Search</xsl:variable>
    <xsl:variable name="sep_bar_adv_text">Advanced Search</xsl:variable>
    <xsl:variable name="sep_bar_error_text">Error</xsl:variable>

    <!-- **********************************************************************
        Search Parameters (do not customize)
        ********************************************************************** -->

    <!-- *** num_results: actual num_results per page *** -->
    <xsl:variable name="num_results">
        <xsl:choose>
            <xsl:when test="/GSP/PARAM[(@name='num') and (@value!='')]">
                <xsl:value-of select="/GSP/PARAM[@name='num']/@value"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="10"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <!-- **********************************************************************
        Separation bar variables (used in advanced search header and result page)
        ********************************************************************** -->
    <xsl:variable name="sep_bar_border_color">
        <xsl:choose>
            <xsl:when test="$choose_sep_bar = 'ltblue'">#3366cc</xsl:when>
            <xsl:when test="$choose_sep_bar = 'blue'">#3366cc</xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$global_bg_color"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <xsl:variable name="sep_bar_bg_color">
        <xsl:choose>
            <xsl:when test="$choose_sep_bar = 'ltblue'">#ECF4D9</xsl:when>
            <xsl:when test="$choose_sep_bar = 'blue'">#3366cc</xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$global_bg_color"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <xsl:variable name="sep_bar_text_color">
        <xsl:choose>
            <xsl:when test="$choose_sep_bar = 'ltblue'">#000000</xsl:when>
            <xsl:when test="$choose_sep_bar = 'blue'">#ffffff</xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$global_text_color"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <!-- **********************************************************************
        Global Style variables (can be customized): '' for using browser's default
        ********************************************************************** -->

    <xsl:variable name="global_font">Verdana, Arial, Helvetica, sans-serif</xsl:variable>
    <xsl:variable name="global_font_size">11px</xsl:variable>
    <xsl:variable name="global_bg_color">#ffffff</xsl:variable>
    <xsl:variable name="global_text_color">#000000</xsl:variable>
    <xsl:variable name="global_link_color">#0000cc</xsl:variable>
    <xsl:variable name="global_vlink_color">#551a8b</xsl:variable>
    <xsl:variable name="global_alink_color">#ff0000</xsl:variable>

    <!-- *** home_url: search? + collection info + &proxycustom=<HOME/> *** -->
    <xsl:variable name="home_url">search?<xsl:value-of select="$base_url"
        />&amp;proxycustom=&lt;HOME/&gt;</xsl:variable>

    <!-- *** base_url: collection info *** -->
    <xsl:variable name="base_url">
        <xsl:for-each
            select="/response/GSP/PARAM[@name = 'client' or
            
            @name = 'site' or
            @name = 'num' or
            @name = 'output' or
            @name = 'proxystylesheet' or
            @name = 'access' or
            @name = 'lr' or
            @name = 'ie']">
            <xsl:value-of select="@name"/>=<xsl:value-of select="@original_value"/>
            <xsl:if test="position() != last()">&amp;</xsl:if>
        </xsl:for-each>
    </xsl:variable>

    <!-- *** keymatch suggestions *** -->
    <xsl:variable name="show_keymatch">1</xsl:variable>
    <xsl:variable name="keymatch_text">KeyMatch</xsl:variable>
    <xsl:variable name="keymatch_text_color">#2255aa</xsl:variable>
    <xsl:variable name="keymatch_bg_color">#e8e8ff</xsl:variable>

    <xsl:variable name="access">
        <xsl:choose>
            <xsl:when
                test="/response/GSP/PARAM[(@name='access') and ((@value='s') or (@value='a'))]">
                <xsl:value-of select="/response/GSP/PARAM[@name='access']/@original_value"/>
            </xsl:when>
            <xsl:otherwise>p</xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <!-- **********************************************************************
        Result elements (can be customized)
        - whether to show an element ('1' for yes, '0' for no)
        - font/size/color ('' for using style of the context)
        ********************************************************************** -->

    <!-- *** result title and snippet *** -->
    <xsl:variable name="show_res_title">1</xsl:variable>
    <xsl:variable name="res_title_color">#0000cc</xsl:variable>
    <xsl:variable name="res_title_size">11px</xsl:variable>
    <xsl:variable name="show_res_snippet">1</xsl:variable>
    <xsl:variable name="res_snippet_size">80%</xsl:variable>

    <!-- *** keyword match (in title or snippet) *** -->
    <xsl:variable name="res_keyword_color"/>
    <xsl:variable name="res_keyword_size"/>
    <xsl:variable name="res_keyword_format">b</xsl:variable>
    <!-- 'b' for bold -->

    <!-- *** link URL *** -->
    <xsl:variable name="show_res_url">1</xsl:variable>
    <xsl:variable name="res_url_color">#008000</xsl:variable>
    <xsl:variable name="res_url_size">-1</xsl:variable>
    <xsl:variable name="truncate_result_urls">1</xsl:variable>
    <!--<xsl:variable name="truncate_result_url_length">100</xsl:variable>-->
    <xsl:variable name="truncate_result_url_length">80</xsl:variable>

    <!-- *** misc elements *** -->
    <xsl:variable name="show_meta_tags">0</xsl:variable>
    <xsl:variable name="show_res_size">1</xsl:variable>
    <xsl:variable name="show_res_date">1</xsl:variable>
    <xsl:variable name="show_res_cache">1</xsl:variable>

    <!-- *** used in result cache link, similar pages link, and description *** -->
    <xsl:variable name="faint_color">#7777cc</xsl:variable>



    <xsl:variable name="search_box_size">32</xsl:variable>
    <!-- *** choose search button type: 'text' or 'image' *** -->
    <xsl:variable name="choose_search_button">text</xsl:variable>
    <xsl:variable name="search_button_text">Google Search</xsl:variable>
    <xsl:variable name="search_button_image_url"/>
    <xsl:variable name="search_collections_xslt">1</xsl:variable>

    <!-- *** customize provided result page header *** -->
    <xsl:variable name="show_swr_link">1</xsl:variable>
    <xsl:variable name="swr_search_anchor_text">Search Within Results</xsl:variable>
    <xsl:variable name="show_result_page_adv_link">1</xsl:variable>
    <xsl:variable name="adv_search_anchor_text">Advanced Search</xsl:variable>
    <xsl:variable name="show_result_page_help_link">1</xsl:variable>
    <xsl:variable name="search_help_anchor_text">Search Tips</xsl:variable>
    <xsl:variable name="show_alerts_link">0</xsl:variable>
    <xsl:variable name="alerts_anchor_text">Alerts</xsl:variable>

    <!-- *** Google Desktop integration *** -->
    <xsl:variable name="egds_show_search_tabs">1</xsl:variable>
    <xsl:variable name="egds_appliance_tab_label">Appliance</xsl:variable>
    <xsl:variable name="egds_show_desktop_results">1</xsl:variable>

    <!-- **********************************************************************
        Variables for reformatting keyword-match display (do not customize)
        ********************************************************************** -->
    <xsl:variable name="keyword_orig_start" select="'&lt;b&gt;'"/>
    <xsl:variable name="keyword_orig_end" select="'&lt;/b&gt;'"/>

    <xsl:variable name="keyword_reformat_start">
        <xsl:if test="$res_keyword_format">
            <xsl:text>&lt;</xsl:text>
            <xsl:value-of select="$res_keyword_format"/>
            <xsl:text>&gt;</xsl:text>
        </xsl:if>
        <xsl:if test="($res_keyword_size) or ($res_keyword_color)">
            <xsl:text>&lt;font</xsl:text>
            <xsl:if test="$res_keyword_size">
                <xsl:text> size="</xsl:text>
                <xsl:value-of select="$res_keyword_size"/>
                <xsl:text>"</xsl:text>
            </xsl:if>
            <xsl:if test="$res_keyword_color">
                <xsl:text> color="</xsl:text>
                <xsl:value-of select="$res_keyword_color"/>
                <xsl:text>"</xsl:text>
            </xsl:if>
            <xsl:text>&gt;</xsl:text>
        </xsl:if>
    </xsl:variable>

    <xsl:variable name="keyword_reformat_end">
        <xsl:if test="($res_keyword_size) or ($res_keyword_color)">
            <xsl:text>&lt;/font&gt;</xsl:text>
        </xsl:if>
        <xsl:if test="$res_keyword_format">
            <xsl:text>&lt;/</xsl:text>
            <xsl:value-of select="$res_keyword_format"/>
            <xsl:text>&gt;</xsl:text>
        </xsl:if>
    </xsl:variable>

    <!-- *** swr_search_url: search? + $search_url + as_q=$q *** -->
    <xsl:variable name="swr_search_url">search?<xsl:value-of select="$search_url"
            />&amp;swrnum=<xsl:value-of select="/response/GSP/RES/M"/></xsl:variable>

    <!-- *** adv_search_url: search? + $search_url + as_q=$q *** -->
    <xsl:variable name="adv_search_url">search?<xsl:value-of select="$search_url"
        />&amp;proxycustom=&lt;ADVANCED/&gt;</xsl:variable>


    <!-- *** filter_url: everything except resetting "filter=" *** -->
    <xsl:variable name="filter_url">search?<xsl:for-each
            select="/GSP/PARAM[(@name != 'filter') and
        (@name != 'epoch' or $is_test_search != '') and
        not(starts-with(@name, 'metabased_'))]">
            <xsl:value-of select="@name"/>
            <xsl:text>=</xsl:text>
            <xsl:value-of select="@original_value"/>
            <xsl:if test="position() != last()">
                <xsl:text disable-output-escaping="yes">&amp;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text disable-output-escaping="yes">&amp;filter=</xsl:text>
    </xsl:variable>

    <!-- *** search_url *** -->
    <xsl:variable name="search_url">
        <xsl:for-each select="/response/GSP/PARAM[(@name = 'q') or (@name = 'as_sitesearch')]">
            <xsl:choose>
                <xsl:when test="@name = 'as_sitesearch'">
                    <xsl:text>site=</xsl:text>
                    <xsl:value-of select="@original_value"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="@name"/>
                    <xsl:text>=</xsl:text>
                    <xsl:value-of select="@original_value"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:if test="position() != last()">
                <xsl:text disable-output-escaping="yes">&amp;</xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:variable>

    <!-- *** synonym_url: does not include q, as_q, and start elements *** -->
    <xsl:variable name="synonym_url">
        <xsl:for-each
            select="/GSP/PARAM[(@name != 'q') and
        (@name != 'as_q') and
        (@name != 'swrnum') and
        
        (@name != 'ie') and
        (@name != 'start') and
        (@name != 'epoch' or $is_test_search != '') and
        not(starts-with(@name, 'metabased_'))]">
            <xsl:value-of select="@name"/>
            <xsl:text>=</xsl:text>
            <xsl:value-of select="@original_value"/>
            <xsl:if test="position() != last()">
                <xsl:text disable-output-escaping="yes">&amp;</xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:variable>

    <!-- *** if this is a test search (help variable)-->
    <xsl:variable name="is_test_search" select="/response/GSP/PARAM[@name='testSearch']/@value"/>

    <!-- *** help_url: search tip URL (html file) *** -->
    <xsl:variable name="help_url">/user_help.html</xsl:variable>

    <!-- *** alerts_url: Alerts URL (html file) *** -->
    <xsl:variable name="alerts_url">/alerts</xsl:variable>


    <!-- *** show secure results radio button *** -->
    <xsl:variable name="show_secure_radio">0</xsl:variable>
    <xsl:template name="nbsp4">
        <xsl:call-template name="nbsp3"/>
        <xsl:call-template name="nbsp"/>
    </xsl:template>


    <!-- **********************************************************************
        Empty result set (can be customized)
        ********************************************************************** -->
    <xsl:template name="no_RES">
        <xsl:param name="query"/>

        <!-- *** Output Google Desktop results (if enabled and any available) *** -->
        <xsl:if test="$egds_show_desktop_results != '0'">
            <xsl:call-template name="desktop_results"/>
        </xsl:if>

        <span class="gsa_results">
            <br/> Your search - <b>
                <xsl:value-of select="$query"/>
            </b> - did not match any documents. <br/> No pages were found containing
                    <b>"<xsl:value-of select="$query"/>"</b>. <br/>
            <br/> Suggestions: <ul>
                <li>Make sure all words are spelled correctly.</li>
                <li>Try different keywords.</li>
                <xsl:if test="/GSP/PARAM[(@name='access') and(@value='a')]">
                    <li>Make sure your security credentials are correct.</li>
                </xsl:if>
                <li>Try more general keywords.</li>
            </ul>
        </span>

    </xsl:template>

    <!-- **********************************************************************
        A single result (do not customize)
        ********************************************************************** -->
    <xsl:template match="R">
        <xsl:param name="query"/>



        <xsl:variable name="display_url_tmp" select="substring-after(UD, '://')"/>
        <xsl:variable name="display_url">
            <xsl:choose>
                <xsl:when test="$display_url_tmp">
                    <xsl:value-of select="$display_url_tmp"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="substring-after(U, '://')"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:variable name="escaped_url" select="substring-after(UE, '://')"/>
        <xsl:variable name="protocol" select="substring-before(U, '://')"/>
        <xsl:variable name="full_url" select="UE"/>
        <xsl:variable name="crowded_url" select="HN/@U"/>
        <xsl:variable name="crowded_display_url" select="HN"/>
        <xsl:variable name="lower" select="'abcdefghijklmnopqrstuvwxyz'"/>
        <xsl:variable name="upper" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>

        <xsl:variable name="temp_url" select="substring-after(U, '://')"/>
        <xsl:variable name="url_indexed" select="not(starts-with($temp_url, 'noindex!/'))"/>
        <xsl:variable name="stripped_url">
            <xsl:choose>
                <xsl:when test="$truncate_result_urls != '0'">
                    <xsl:call-template name="truncate_url">
                        <xsl:with-param name="t_url" select="$display_url"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$display_url"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>


        <!-- *** Indent as required (only supports 2 levels) *** -->
        <xsl:if test="@L='2'">
            <xsl:text disable-output-escaping="yes">&lt;blockquote class=&quot;g&quot;&gt;</xsl:text>
        </xsl:if>

        <!-- *** Result Header *** -->
        <p class="g">

            <!-- *** Result Title (including PDF tag and hyperlink) *** -->
            <xsl:if test="$show_res_title != '0'">
                <span class="gsa_results">
                    <b>
                        <xsl:choose>
                            <xsl:when test="@MIME='text/html' or @MIME='' or not(@MIME)"/>
                            <xsl:when test="@MIME='text/plain'">[TEXT]</xsl:when>
                            <xsl:when test="@MIME='application/rtf'">[RTF]</xsl:when>
                            <xsl:when test="@MIME='application/pdf'">[PDF]</xsl:when>
                            <xsl:when test="@MIME='application/postscript'">[PS]</xsl:when>
                            <xsl:when test="@MIME='application/vnd.ms-powerpoint'">[MS POWERPOINT]</xsl:when>
                            <xsl:when test="@MIME='application/vnd.ms-excel'">[MS EXCEL]</xsl:when>
                            <xsl:when test="@MIME='application/msword'">[MS WORD]</xsl:when>
                            <xsl:otherwise>
                                <xsl:variable name="extension">
                                    <xsl:call-template name="last_substring_after">
                                        <xsl:with-param name="string"
                                            select="substring-after(
                                        substring-after(U,'://'),
                                        '/')"/>
                                        <xsl:with-param name="separator" select="'.'"/>
                                        <xsl:with-param name="fallback" select="'UNKNOWN'"/>
                                    </xsl:call-template>
                                </xsl:variable> [<xsl:value-of
                                    select="translate($extension,$lower,$upper)"/>] </xsl:otherwise>
                        </xsl:choose>
                    </b>
                </span>
                <xsl:text> </xsl:text>

                <xsl:if test="$url_indexed">

                    <xsl:text disable-output-escaping="yes">&lt;a href="</xsl:text>

                    <xsl:choose>
                        <xsl:when test="starts-with(U, $db_url_protocol)">
                            <xsl:value-of disable-output-escaping="yes"
                                select="concat('db/', substring-after(U,'://'))"/>
                        </xsl:when>
                        <!-- *** URI for smb or NFS must be escaped because it appears in the URI query *** -->
                        <xsl:when test="$protocol='nfs' or $protocol='smb'">
                            <xsl:value-of disable-output-escaping="yes"
                                select="concat($protocol,'/',
                                substring-after(U,'://'))"
                            />
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of disable-output-escaping="yes" select="U"/>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
                </xsl:if>
                <span class="gsa_results">
                    <xsl:choose>
                        <xsl:when test="T">
                            <xsl:call-template name="reformat_keyword">
                                <xsl:with-param name="orig_string" select="T"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="$stripped_url"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </span>
                <xsl:if test="$url_indexed">
                    <xsl:text disable-output-escaping="yes">&lt;/a&gt;</xsl:text>
                </xsl:if>
            </xsl:if>


            <!-- *** Snippet Box *** -->
            <table cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td class="gsa_results">
                        <xsl:if test="$show_res_snippet != '0'">
                            <xsl:call-template name="reformat_keyword">
                                <xsl:with-param name="orig_string" select="S"/>
                            </xsl:call-template>
                        </xsl:if>

                        <!-- *** Meta tags *** -->
                        <xsl:if test="$show_meta_tags != '0'">
                            <xsl:apply-templates select="MT"/>
                        </xsl:if>

                        <!-- *** URL *** -->
                        <br/>
                        <font color="{$res_url_color}" size="{$res_url_size}">
                            <xsl:choose>
                                <xsl:when test="not($url_indexed)">
                                    <xsl:if
                                        test="($show_res_size!='0') or
                                        ($show_res_date!='0') or
                                        ($show_res_cache!='0')">
                                        <xsl:text>Not Indexed:</xsl:text>
                                        <xsl:value-of select="$stripped_url"/>
                                    </xsl:if>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:if test="$show_res_url != '0'">
                                        <xsl:value-of select="$stripped_url"/>
                                    </xsl:if>
                                </xsl:otherwise>
                            </xsl:choose>
                        </font>

                        <!-- *** Miscellaneous (- size - date - cache) *** -->
                        <xsl:if test="$url_indexed">
                            <xsl:apply-templates select="HAS/C">
                                <xsl:with-param name="stripped_url" select="$stripped_url"/>
                                <xsl:with-param name="escaped_url" select="$escaped_url"/>
                                <xsl:with-param name="query" select="$query"/>
                                <xsl:with-param name="mime" select="@MIME"/>
                                <xsl:with-param name="date" select="FS[@NAME='date']/@VALUE"/>
                            </xsl:apply-templates>
                        </xsl:if>


                        <!-- *** Link to more links from this site *** -->
                        <xsl:if test="HN">
                            <br/> [ <a class="f"
                                href="search?as_sitesearch={$crowded_url}&amp;{
                                $search_url}"
                                >More results from <xsl:value-of select="$crowded_display_url"/></a>
                            ] <!-- *** Link to aggregated results from database source *** -->
                            <xsl:if test="starts-with($crowded_url, $db_url_protocol)"> [ <a
                                    class="f"
                                    href="dbaggr?sitesearch={$crowded_url}&amp;{
                                    $search_url}"
                                    >View all data</a> ] </xsl:if>
                        </xsl:if>


                        <!-- *** Result Footer *** -->
                    </td>
                </tr>
            </table>
        </p>

        <!-- *** End indenting as required (only supports 2 levels) *** -->
        <xsl:if test="@L='2'">
            <xsl:text disable-output-escaping="yes">&lt;/blockquote&gt;</xsl:text>
        </xsl:if>

    </xsl:template>

    <xsl:template match="GSP">

        <xsl:call-template name="analytics"/>
        <xsl:call-template name="swr_page_header"/>
        <hr/>
        <!-- *** Handle results (if any) *** -->
        <xsl:choose>
            <xsl:when test="RES or GM or Spelling or Synonyms or CT or /GSP/ENTOBRESULTS">
                <xsl:call-template name="results">
                    <xsl:with-param name="query" select="Q"/>
                    <xsl:with-param name="time" select="TM"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="Q=''"> </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="no_RES">
                    <xsl:with-param name="query" select="Q"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>

        <xsl:call-template name="copyright"/>


    </xsl:template>

    <xsl:template name="analytics">
        <xsl:if test="string-length($analytics_account) != '0'">
            <script src="{$analytics_script_url}" type="text/javascript"/>
            <script type="text/javascript">
                <xsl:comment> _uacct = "<xsl:value-of select="$analytics_account"/>";
                    urchinTracker(); //</xsl:comment>
            </script>
        </xsl:if>
    </xsl:template>

    <!-- **********************************************************************
        Search within results page header (can be customized): logo and search box
        ********************************************************************** -->
    <xsl:template name="swr_page_header">
        <table border="0" cellpadding="0" cellspacing="0">
            <xsl:if test="$show_logo != '0'">
                <tr>
                    <td rowspan="3" valign="top">
                        <xsl:call-template name="nbsp3"/>
                    </td>
                </tr>
            </xsl:if>
            <xsl:if test="$show_top_search_box != '0'">
                <tr>
                    <td valign="middle">
                        <xsl:call-template name="search_box">
                            <xsl:with-param name="type" select="'swr'"/>
                        </xsl:call-template>
                    </td>
                </tr>
            </xsl:if>
        </table>
    </xsl:template>

    <!-- **********************************************************************
        Synonym suggestions in result page (do not customize)
        ********************************************************************** -->
    <xsl:template name="synonyms">
        <xsl:if test="/GSP/Synonyms/OneSynonym">
            <p>
                <span class="p">
                    <font color="{$synonyms_text_color}">
                        <xsl:value-of select="$synonyms_text"/>
                        <xsl:call-template name="nbsp"/>
                    </font>
                </span>
                <xsl:for-each select="/GSP/Synonyms/OneSynonym">
                    <a href="search?q={@q}&amp;{$synonym_url}">
                        <xsl:value-of disable-output-escaping="yes" select="."/>
                    </a>
                    <xsl:text> </xsl:text>
                </xsl:for-each>
            </p>
        </xsl:if>
    </xsl:template>

    <xsl:template name="truncate_chop_path">
        <xsl:param name="path"/>
        <xsl:param name="path_limit"/>

        <xsl:choose>
            <xsl:when test="string-length($path) &lt;= $path_limit">
                <xsl:value-of select="$path"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="truncate_chop_path">
                    <xsl:with-param name="path" select="substring-after($path, '/')"/>
                    <xsl:with-param name="path_limit" select="$path_limit"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>

    <xsl:template name="truncate_find_last_token">
        <xsl:param name="t_url"/>

        <xsl:choose>
            <xsl:when test="contains($t_url, '/')">
                <xsl:call-template name="truncate_find_last_token">
                    <xsl:with-param name="t_url" select="substring-after($t_url, '/')"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$t_url"/>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>

    <!-- **********************************************************************
        Truncation functions (do not customize)
        ********************************************************************** -->
    <xsl:template name="truncate_url">
        <xsl:param name="t_url"/>

        <xsl:choose>
            <xsl:when test="string-length($t_url) &lt; $truncate_result_url_length">
                <xsl:value-of select="$t_url"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:variable name="first" select="substring-before($t_url, '/')"/>
                <xsl:variable name="last">
                    <xsl:call-template name="truncate_find_last_token">
                        <xsl:with-param name="t_url" select="$t_url"/>
                    </xsl:call-template>
                </xsl:variable>
              <xsl:variable name="path_limit"
              select="$truncate_result_url_length - (string-length($first) + string-length($last) + 1)"/>
                
                <xsl:variable name="last_limit"
                    select="(string-length($last)*.5)"/>
                <xsl:choose>
                    <xsl:when test="$path_limit &lt;= 0"> 
                      <!--<xsl:value-of
                            select="concat(substring($t_url, 1, $truncate_result_url_length), '...')"
                            />  -->
                        <xsl:value-of select="concat($first,'/.../')"/>
                        <xsl:value-of
                            select="substring($last, $last_limit)"
                        />  
                        <!-- <xsl:value-of select="concat($first, '/../',$last)"/>  -->
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:variable name="chopped_path">
                            <xsl:call-template name="truncate_chop_path">
                                <xsl:with-param name="path"
                                    select="substring($t_url, string-length($first) + 2, string-length($t_url) - (string-length($first) + string-length($last) + 1))"/>
                                <xsl:with-param name="path_limit" select="$path_limit"/>
                            </xsl:call-template>
                        </xsl:variable>
                        <!-- <xsl:value-of select="concat($first, '/.../', $chopped_path, $last)"/> -->
                        <xsl:value-of select="concat($first, '/../',$last)"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>

    <!-- **********************************************************************
        Utility functions (do not customize)
        ********************************************************************** -->

    <!-- *** Find the substring after the last occurence of a separator *** -->
    <xsl:template name="last_substring_after">

        <xsl:param name="string"/>
        <xsl:param name="separator"/>
        <xsl:param name="fallback"/>

        <xsl:variable name="newString" select="substring-after($string, $separator)"/>

        <xsl:choose>
            <xsl:when test="$newString!=''">
                <xsl:call-template name="last_substring_after">
                    <xsl:with-param name="string" select="$newString"/>
                    <xsl:with-param name="separator" select="$separator"/>
                    <xsl:with-param name="fallback" select="$newString"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$fallback"/>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>

    <!-- **********************************************************************
        Logo template (can be customized)
        ********************************************************************** -->
    <xsl:template name="logo">
        <a href="{$home_url}">
            <img src="{$logo_url}" width="{$logo_width}" height="{$logo_height}"
                alt="Go to Google Home" border="0"/>
        </a>
    </xsl:template>

    <!-- **********************************************************************
        Search box input form (Types: std_top, std_bottom, home, swr)
        ********************************************************************** -->
    <xsl:template name="search_box">
        <xsl:param name="type"/>

        <xsl:variable name="response_gsp" select="/response/GSP"/>
        <!-- Conserveonline -->

        <form name="gs" method="get" action="/search">
            <table border="0" cellpadding="0" cellspacing="0" class="gsa_results">
                <xsl:if
                    test="($egds_show_search_tabs != '0') and (($type = 'home') or ($type = 'std_top'))">
                    <tr>
                        <td>
                            <table cellpadding="4" cellspacing="0">
                                <tr>
                                    <td>
                                        <xsl:call-template name="desktop_tab"/>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="($type = 'swr')">
                    <tr>
                        <td>
                            <table cellpadding="4" cellspacing="0">
                                <tr>
                                    <td class="gsa_results">
                                        <xsl:choose>
                                            <xsl:when test="(Q = '')"> </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:choose>
                                                  <xsl:when test="RES/M"> There were about <b>
                                                  <xsl:value-of select="RES/M"/>
                                                  </b> results for <b>
                                                  <xsl:value-of
                                                  select="$response_gsp/PARAM[@name='q']/@value"
                                                  />
                                                  </b>. </xsl:when>
                                                  <xsl:otherwise> There were <b>0</b> results for <b>
                                                  <xsl:value-of
                                                  select="$response_gsp/PARAM[@name='q']/@value"
                                                  />
                                                  </b>. </xsl:otherwise>
                                                </xsl:choose>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </xsl:if>
                <tr>
                    <td>
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td valign="middle" class="gsa_results">
                                    <font size="-1">
                                        <xsl:choose>
                                            <xsl:when test="($type = 'swr')">
                                                <input type="text" name="q"
                                                  size="{$search_box_size}" maxlength="256"
                                                  value="{$response_gsp/PARAM[@name='q']/@value}"
                                                />
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <input type="text" name="q"
                                                  size="{$search_box_size}" maxlength="256"
                                                  value="{$response_gsp/PARAM[@name='q']/@value}"
                                                />
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </font>
                                </td>
                                <xsl:call-template name="collection_menu"/>
                                <td valign="middle">
                                    <font size="-1">
                                        <xsl:call-template name="nbsp"/>
                                        <xsl:choose>
                                            <xsl:when test="$choose_search_button = 'image'">
                                                <input type="image"
                                                  class="btnGreen btnGreenWidth130" name="btnG"
                                                  src="{$search_button_image_url}" valign="bottom"
                                                  width="60" height="26" border="0"
                                                  value="{$search_button_text}"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                
                                                
                                                <input type="submit" name="btnG" value="Search COL"  class="gsa-result-btn_display"/>
                                                
                                             
                                                
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </font>
                                </td>

                            </tr>
                            <xsl:if test="$show_secure_radio != '0'">
                                <tr>
                                    <td colspan="2">
                                        <font size="-1">Search: <xsl:choose>
                                                <xsl:when test="$access='p'">
                                                  <label><input type="radio" name="access"
                                                  value="p" checked="checked"/>public
                                                  content</label>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                  <label><input type="radio" name="access"
                                                  value="p"/>public content</label>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                            <xsl:choose>
                                                <xsl:when test="$access='a'">
                                                  <label><input type="radio" name="access"
                                                  value="a" checked="checked"/>public and
                                                  secure content</label>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                  <label><input type="radio" name="access"
                                                  value="a"/>public and secure
                                                  content</label>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </font>
                                    </td>
                                </tr>
                            </xsl:if>
                        </table>
                    </td>
                </tr>
            </table>
            <xsl:text>
            </xsl:text>
            <xsl:call-template name="form_params"/>
        </form>
    </xsl:template>

    <!-- **********************************************************************
        Spelling suggestions in result page (do not customize)
        ********************************************************************** -->
    <xsl:template name="spelling">
        <xsl:if test="/GSP/Spelling/Suggestion">
            <p>
                <span class="p">
                    <font color="{$spelling_text_color}">
                        <xsl:value-of select="$spelling_text"/>
                        <xsl:call-template name="nbsp"/>
                    </font>
                </span>
                <a
                    href="search?q={/GSP/Spelling/Suggestion[1]/@qe}&amp;spell=1&amp;{$base_url}">
                    <xsl:value-of disable-output-escaping="yes" select="/GSP/Spelling/Suggestion[1]"
                    />
                </a>
            </p>
        </xsl:if>
    </xsl:template>

    <!-- **********************************************************************
        Sort-by criteria: sort by date/relevance
        ********************************************************************** -->
    <xsl:template name="sort_by">
        <xsl:variable name="sort_by_url">
            <xsl:for-each
                select="/GSP/PARAM[(@name != 'sort') and
            (@name != 'start') and
            (@name != 'epoch' or $is_test_search != '') and
            not(starts-with(@name, 'metabased_'))]">
                <xsl:value-of select="@name"/>
                <xsl:text>=</xsl:text>
                <xsl:value-of select="@original_value"/>
                <xsl:if test="position() != last()">
                    <xsl:text disable-output-escaping="yes">&amp;</xsl:text>
                </xsl:if>
            </xsl:for-each>
        </xsl:variable>

        <xsl:variable name="sort_by_relevance_url">
            <xsl:value-of select="$sort_by_url"/>&amp;sort=date%3AD%3AL%3Ad1</xsl:variable>

        <xsl:variable name="sort_by_date_url">
            <xsl:value-of select="$sort_by_url"/>&amp;sort=date%3AD%3AS%3Ad1</xsl:variable>


    </xsl:template>

    <!-- **********************************************************************
        Utility functions for generating html entities
        ********************************************************************** -->
    <xsl:template name="nbsp">
        <xsl:text disable-output-escaping="yes">&amp;nbsp;</xsl:text>
    </xsl:template>
    <xsl:template name="nbsp3">
        <xsl:call-template name="nbsp"/>
        <xsl:call-template name="nbsp"/>
        <xsl:call-template name="nbsp"/>
    </xsl:template>

    <!-- **********************************************************************
        Utility function for constructing copyright text (do not customize)
        ********************************************************************** -->
    <xsl:template name="copyright">
        <!--<center>
            <br/><br/>
            <p>
                <font face="arial,sans-serif" size="-1" color="#2f2f2f">
                    Powered by Google Search Appliance</font>
            </p>
        </center>-->
    </xsl:template>

    <!-- **********************************************************************
        Google Desktop for Enterprise integration templates
        ********************************************************************** -->
    <xsl:template name="desktop_tab">

        <!-- *** Show the Google tabs *** -->

        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1"
                href="http://www.google.com/search?q={$qval}">Web</a>
        </font>

        <xsl:call-template name="nbsp4"/>

        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1"
                href="http://images.google.com/images?q={$qval}">Images</a>
        </font>

        <xsl:call-template name="nbsp4"/>

        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1"
                href="http://groups.google.com/groups?q={$qval}">Groups</a>
        </font>

        <xsl:call-template name="nbsp4"/>

        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1"
                href="http://news.google.com/news?q={$qval}">News</a>
        </font>

        <xsl:call-template name="nbsp4"/>

        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1"
                href="http://froogle.google.com/froogle?q={$qval}">Froogle</a>
        </font>

        <xsl:call-template name="nbsp4"/>

        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1"
                href="http://local.google.com/local?q={$qval}">Local</a>
        </font>

        <xsl:call-template name="nbsp4"/>

        <!-- *** Show the desktop and web tabs *** -->

        <xsl:if test="CUSTOM/HOME">
            <xsl:comment>trh2</xsl:comment>
        </xsl:if>
        <xsl:if test="Q">
            <xsl:comment>trl2</xsl:comment>
        </xsl:if>

        <!-- *** Show the appliance tab *** -->
        <font size="-1">
            <b>
                <xsl:value-of select="$egds_appliance_tab_label"/>
            </b>
        </font>

    </xsl:template>

    <xsl:template name="desktop_results">
        <xsl:comment>tro2</xsl:comment>
    </xsl:template>

    <!-- *** space_normalized_query: q = /response/GSP/Q *** -->
    <xsl:variable name="qval">
        <xsl:value-of select="/response/GSP/Q"/>
    </xsl:variable>

    <xsl:variable name="space_normalized_query">
        <xsl:value-of select="normalize-space($qval)" disable-output-escaping="yes"/>
    </xsl:variable>

    <!-- **********************************************************************
        Bottom search box (do not customized)
        ********************************************************************** -->
    <xsl:template name="bottom_search_box">
        <br clear="all"/>
        <br/>

       <!-- <table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="{$sep_bar_bg_color}">
            <tr>
                <td class="gsaBottomBox" nowrap="1" bgcolor="{$sep_bar_bg_color}" align="left">
                    <br/>
                    <xsl:call-template name="search_box">
                        <xsl:with-param name="type" select="'std_bottom'"/>
                    </xsl:call-template>
                    <br/>
                </td>
            </tr>
        </table>-->
  
    </xsl:template> 

    <!-- **********************************************************************
        Collection menu beside the search box
        ********************************************************************** -->
    <xsl:template name="collection_menu">
        <xsl:if test="$search_collections_xslt != ''"> </xsl:if>
    </xsl:template>

    <!-- **********************************************************************
        OneBox results (if any)
        ********************************************************************** -->
    <xsl:template name="onebox">
        <xsl:for-each select="/GSP/ENTOBRESULTS">
            <xsl:apply-templates/>
        </xsl:for-each>
    </xsl:template>

    <!-- **********************************************************************
        Output all results
        ********************************************************************** -->
    <xsl:template name="results">
        <xsl:param name="query"/>
        <xsl:param name="time"/>

        <!-- *** Add top navigation/sort-by bar *** -->
        <xsl:if test="($show_top_navigation != '0') or ($show_sort_by != '0')">
            <xsl:if test="RES">
                <!-- there might be onebox results but no RES  -->
                <table width="100%">
                    <tr>
                        <xsl:if test="$show_top_navigation != '0'">
                            <td align="center" class="gsa_results_menu">
                                <xsl:call-template name="google_navigation">
                                    <xsl:with-param name="prev" select="RES/NB/PU"/>
                                    <xsl:with-param name="next" select="RES/NB/NU"/>
                                    <xsl:with-param name="view_begin" select="RES/@SN"/>
                                    <xsl:with-param name="view_end" select="RES/@EN"/>
                                    <xsl:with-param name="guess" select="RES/M"/>
                                    <xsl:with-param name="navigation_style" select="'top'"/>
                                </xsl:call-template>
                            </td>
                        </xsl:if>
                        <xsl:if test="$show_sort_by != '0'">
                            <td align="right">
                                <xsl:call-template name="sort_by"/>
                            </td>
                        </xsl:if>
                    </tr>
                </table>
            </xsl:if>
        </xsl:if>

        <!-- *** Handle OneBox results, if any ***-->
        <xsl:if test="$show_onebox != '0'">
            <xsl:if test="/GSP/ENTOBRESULTS">
                <xsl:call-template name="onebox"/>
            </xsl:if>
        </xsl:if>

        <!-- *** Handle spelling suggestions, if any *** -->
        <xsl:if test="$show_spelling != '0'">
            <xsl:call-template name="spelling"/>
        </xsl:if>

        <!-- *** Handle synonyms, if any *** -->
        <xsl:if test="$show_synonyms != '0'">
            <xsl:call-template name="synonyms"/>
        </xsl:if>

        <!-- *** Output Google Desktop results (if enabled and any available) *** -->
        <xsl:if test="$egds_show_desktop_results != '0'">
            <xsl:call-template name="desktop_results"/>
        </xsl:if>

        <!-- *** Output results details *** -->
        <div>
            <!-- for keymatch results -->
            <xsl:if test="$show_keymatch != '0'">
                <xsl:apply-templates select="/GSP/GM"/>
            </xsl:if>

            <!-- for real results -->
            <xsl:apply-templates select="RES/R">
                <xsl:with-param name="query" select="$query"/>
            </xsl:apply-templates>

            <!-- *** Filter note (if needed) *** -->
            <xsl:if test="(RES/FI) and (not(RES/NB/NU))"> </xsl:if>
        </div>

        <!-- *** Add bottom navigation *** -->
        <xsl:variable name="nav_style">
            <xsl:choose>
                <xsl:when test="($access='s') or ($access='a')">simple</xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$choose_bottom_navigation"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <table width="100%">
            <tr>
                    <td align="center" class="gsa_results_menu">
        <xsl:call-template name="google_navigation">
            <xsl:with-param name="prev" select="RES/NB/PU"/>
            <xsl:with-param name="next" select="RES/NB/NU"/>
            <xsl:with-param name="view_begin" select="RES/@SN"/>
            <xsl:with-param name="view_end" select="RES/@EN"/>
            <xsl:with-param name="guess" select="RES/M"/>
            <xsl:with-param name="navigation_style" select="$nav_style"/>
        </xsl:call-template>
                    </td>
            </tr>
            </table>

        <!-- *** Bottom search box *** -->
        <xsl:if test="$show_bottom_search_box != '0'">
            <xsl:call-template name="bottom_search_box"/>
        </xsl:if>

    </xsl:template>

    <!-- **********************************************************************
        Reformat the keyword match display in a title/snippet string
        (do not customize)
        ********************************************************************** -->
    <xsl:template name="reformat_keyword">
        <xsl:param name="orig_string"/>

        <xsl:variable name="reformatted_1">
            <xsl:call-template name="replace_string">
                <xsl:with-param name="find" select="$keyword_orig_start"/>
                <xsl:with-param name="replace" select="$keyword_reformat_start"/>
                <xsl:with-param name="string" select="$orig_string"/>
            </xsl:call-template>
        </xsl:variable>

        <xsl:variable name="reformatted_2">
            <xsl:call-template name="replace_string">
                <xsl:with-param name="find" select="$keyword_orig_end"/>
                <xsl:with-param name="replace" select="$keyword_reformat_end"/>
                <xsl:with-param name="string" select="$reformatted_1"/>
            </xsl:call-template>
        </xsl:variable>

        <xsl:value-of disable-output-escaping="yes" select="$reformatted_2"/>

    </xsl:template>

    <!-- *** Find and replace *** -->
    <xsl:template name="replace_string">
        <xsl:param name="find"/>
        <xsl:param name="replace"/>
        <xsl:param name="string"/>
        <xsl:choose>
            <xsl:when test="contains($string, $find)">
                <xsl:value-of select="substring-before($string, $find)"/>
                <xsl:value-of select="$replace"/>
                <xsl:call-template name="replace_string">
                    <xsl:with-param name="find" select="$find"/>
                    <xsl:with-param name="replace" select="$replace"/>
                    <xsl:with-param name="string" select="substring-after($string, $find)"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$string"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- **********************************************************************
        Helper templates for generating Google result navigation (do not customize)
        only shows 10 sets up or down from current view
        ********************************************************************** -->
    <xsl:template name="result_nav">
        <xsl:param name="start" select="'0'"/>
        <xsl:param name="end"/>
        <xsl:param name="current_view"/>
        <xsl:param name="navigation_style"/>

        <!-- *** Choose how to show this result set *** -->
        <xsl:choose>
            <xsl:when test="($start)&lt;(($current_view)-(10*($num_results)))"> </xsl:when>
            <xsl:when
                test="(($current_view)&gt;=($start)) and
                (($current_view)&lt;(($start)+($num_results)))">
                <td>
                    <xsl:if test="$navigation_style = 'google'">
                        <img src="/nav_current.gif" width="16" height="26" alt="Current"/>
                        <br/>
                    </xsl:if>
                    <xsl:if test="$navigation_style = 'link'">
                        <xsl:call-template name="nbsp"/>
                    </xsl:if>
                    <span class="i">
                        <xsl:value-of select="(($start)div($num_results))+1"/>
                    </span>
                    <xsl:if test="$navigation_style = 'link'">
                        <xsl:call-template name="nbsp"/>
                    </xsl:if>
                </td>
            </xsl:when>
            <xsl:otherwise>
                <td>
                    <xsl:if test="$navigation_style = 'link'">
                        <xsl:call-template name="nbsp"/>
                    </xsl:if>
                    <a href="/search?{$search_url}&amp;start={$start}">
                        <xsl:if test="$navigation_style = 'google'">
                            <img src="/nav_page.gif" width="16" height="26" alt="Navigation"
                                border="0"/>
                            <br/>
                        </xsl:if>
                        <xsl:value-of select="(($start)div($num_results))+1"/>
                    </a>
                    <xsl:if test="$navigation_style = 'link'">
                        <xsl:call-template name="nbsp"/>
                    </xsl:if>
                </td>
            </xsl:otherwise>
        </xsl:choose>

        <!-- *** Recursively iterate through result sets to display *** -->
        <xsl:if
            test="((($start)+($num_results))&lt;($end)) and
            ((($start)+($num_results))&lt;(($current_view)+
            (10*($num_results))))">
            <xsl:call-template name="result_nav">
                <xsl:with-param name="start" select="$start+$num_results"/>
                <xsl:with-param name="end" select="$end"/>
                <xsl:with-param name="current_view" select="$current_view"/>
                <xsl:with-param name="navigation_style" select="$navigation_style"/>
            </xsl:call-template>
        </xsl:if>

    </xsl:template>

    <!-- *** form_params: parameters carried by the search input form *** -->
    <xsl:template name="form_params">
        <input type="hidden" name="site" value="{PARAM[@name='as_sitesearch']/@value}"/>
        <!--<xsl:for-each
            select="PARAM[@name != 'q' and
            @name != 'ie' and
            not(contains(@name, 'as_')) and
            @name != 'btnG' and
            @name != 'btnI' and
            @name != 'site' and
            @name != 'filter' and
            @name != 'swrnum' and
            @name != 'start' and
            @name != 'access' and
            @name != 'ip' and
            (@name != 'epoch' or $is_test_search != '') and
            not(starts-with(@name ,'metabased_'))]">
            <input type="hidden" name="{@name}" value="{@value}" />
            
            <xsl:if test="@name = 'oe'">
                <input type="hidden" name="ie" value="{@value}" />
            </xsl:if>
            <xsl:text>
            </xsl:text>
            </xsl:for-each>-->
        <xsl:if test="$search_collections_xslt = '' and PARAM[@name='site']">
            <input type="hidden" name="site" value="{PARAM[@name='site']/@value}"/>
        </xsl:if>
    </xsl:template>
    <!-- **********************************************************************
        Google navigation bar in result page (do not customize)
        ********************************************************************** -->
    <xsl:template name="google_navigation">
        <xsl:param name="prev"/>
        <xsl:param name="next"/>
        <xsl:param name="view_begin"/>
        <xsl:param name="view_end"/>
        <xsl:param name="guess"/>
        <xsl:param name="navigation_style"/>

        <xsl:variable name="fontclass">
            <xsl:choose>
                <xsl:when test="$navigation_style = 'top'">s</xsl:when>
                <xsl:otherwise>b</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <!-- *** Test to see if we should even show navigation *** -->
        <xsl:if test="($prev) or ($next)">

            <!-- *** Start Google result navigation bar *** -->

            <xsl:if test="$navigation_style != 'top'">
                <xsl:text disable-output-escaping="yes">&lt;p=center&gt;
                   </xsl:text>
            </xsl:if>

            <table border="0" cellpadding="0" width="1%" cellspacing="0">
                <tr align="center" valign="top" class="gsa_results">
                   <!-- <xsl:if test="$navigation_style != 'top'">
                        <td valign="bottom" nowrap="1">
                            <font size="-1"> Result Page<xsl:call-template name="nbsp"/>
                            </font>
                        </td>
                    </xsl:if> -->

                    <xsl:variable name="nurl" select="/response/GSP[1]/RES[1]/NB[1]/NU[1]"/>
                    <xsl:variable name="purl" select="/response/GSP[1]/RES[1]/NB[1]/PU[1]"/>
                    <xsl:variable name="baseurl" select="/response/breadcrumbs/base"/>
                    
                    <xsl:variable name="nexturl" select="concat($baseurl, substring-after($nurl, '/'))"/>
                    <xsl:variable name="prevurl" select="concat($baseurl, substring-after($purl, '/'))"/>

                    <!-- *** Show previous navigation, if available *** -->
                    <xsl:choose>
                        <xsl:when test="$prev">
                            <td nowrap="1">

                                <span class="{$fontclass}">
                                    <a
                                        href="{$prevurl}">
                                        <xsl:if test="$navigation_style = 'google'">

                                            <img src="/nav_previous.gif" width="68" height="26"
                                                alt="Previous" border="0"/>
                                            <br/>
                                        </xsl:if>
                                        <xsl:if test="$navigation_style = 'top'">
                                            <xsl:text>&lt;</xsl:text>
                                        </xsl:if>
                                        <xsl:text>Previous</xsl:text>
                                    </a>
                                </span>
                                <xsl:if test="$navigation_style != 'google'">
                                    <xsl:call-template name="nbsp"/>
                                </xsl:if>
                            </td>
                        </xsl:when>
                        <xsl:otherwise>
                            <td nowrap="1">
                                <xsl:if test="$navigation_style = 'google'">
                                    <img src="/nav_first.gif" width="18" height="26" alt="First"
                                        border="0"/>
                                    <br/>
                                </xsl:if>
                            </td>
                        </xsl:otherwise>
                    </xsl:choose>

                    <xsl:if
                        test="($navigation_style = 'google') or
                        ($navigation_style = 'link')">
                        <!-- *** Google result set navigation *** -->
                        <xsl:variable name="mod_end">
                            <xsl:choose>
                                <xsl:when test="$next">
                                    <xsl:value-of select="$guess"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="$view_end"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:variable>

                        <xsl:call-template name="result_nav">
                            <xsl:with-param name="start" select="0"/>
                            <xsl:with-param name="end" select="$mod_end"/>
                            <xsl:with-param name="current_view" select="($view_begin)-1"/>
                            <xsl:with-param name="navigation_style" select="$navigation_style"/>
                        </xsl:call-template>
                    </xsl:if>

                    <!-- *** Show next navigation, if available *** -->
                    <xsl:choose>
                        <xsl:when test="$next">
                            <td nowrap="1">
                                <xsl:if test="$navigation_style != 'google'">
                                    <xsl:call-template name="nbsp"/>
                                </xsl:if>
                                <span class="{$fontclass}">
                                    <a
                                        href="{$nexturl}">
                                        <xsl:if test="$navigation_style = 'google'">

                                            <img src="/nav_next.gif" width="100" height="26"
                                                alt="Next" border="0"/>
                                            <br/>
                                        </xsl:if>
                                        <xsl:text>Next</xsl:text>
                                        <xsl:if test="$navigation_style = 'top'">
                                            <xsl:text>&gt;</xsl:text>
                                        </xsl:if>
                                    </a>
                                </span>
                            </td>
                        </xsl:when>
                        <xsl:otherwise>
                            <td nowrap="1">
                                <xsl:if test="$navigation_style != 'google'">
                                    <xsl:call-template name="nbsp"/>
                                </xsl:if>
                                <xsl:if test="$navigation_style = 'google'">
                                    <img src="/nav_last.gif" width="46" height="26" alt="Last"
                                        border="0"/>
                                    <br/>
                                </xsl:if>
                            </td>
                        </xsl:otherwise>
                    </xsl:choose>

                    <!-- *** End Google result bar *** -->
                </tr>
            </table>

            <xsl:if test="$navigation_style != 'top'">
                <xsl:text disable-output-escaping="yes">&lt;/p&gt;
                   </xsl:text>
            </xsl:if>
        </xsl:if>
    </xsl:template>

    <!-- **********************************************************************
        Global Style (do not customize)
        default font type/size/color, background color, link color
        using HTML CSS (Cascading Style Sheets)
        ********************************************************************** -->
    <xsl:template name="style">
        <style>
            <xsl:comment> body,td,div,.p,a,.d,.s{font-family:<xsl:value-of select="$global_font"/>}
                body,td,div,.p,a,.d{font-size: <xsl:value-of select="$global_font_size"/>}
                    body,div,td,.p,.s{color:<xsl:value-of select="$global_text_color"/>}
                    body,.d,.p,.s{background-color:<xsl:value-of select="$global_bg_color"/>}
                .s{font-size: <xsl:value-of select="$res_snippet_size"/>} .g{margin-top: 1em;
                margin-bottom: 1em} .s td{width:34em} .l{font-size: <xsl:value-of
                    select="$res_title_size"/>} .l{color: <xsl:value-of select="$res_title_color"/>}
                a:link,.w,.w a:link{color:<xsl:value-of select="$global_link_color"/>} .f,.f:link,.f
                    a:link{color:<xsl:value-of select="$faint_color"/>} a:visited,.f
                    a:visited{color:<xsl:value-of select="$global_vlink_color"/>} a:active,.f
                    a:active{color:<xsl:value-of select="$global_alink_color"/>}
                    .t{color:<xsl:value-of select="$sep_bar_text_color"/>}
                    .t{background-color:<xsl:value-of select="$sep_bar_bg_color"/>} .z{display:none}
                .i,.i:link{color:#a90a08} .a,.a:link{color:<xsl:value-of select="$res_url_color"/>}
                div.n {margin-top: 1ex} .n a{font-size: 10pt; color:<xsl:value-of
                    select="$global_text_color"/>} .n .i{font-size: 10pt; font-weight:bold} .q
                a:visited,.q a:link,.q a:active,.q {color:#0000cc;} .b,.b a{font-size: 12pt;
                color:#0000cc; font-weight:bold} .d{margin-right:1em; margin-left:1em;}
                div.oneboxResults {max-height:150px;overflow:hidden;} </xsl:comment>
        </style>
    </xsl:template>

</xsl:stylesheet>
