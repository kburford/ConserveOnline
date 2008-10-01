<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:date="http://exslt.org/dates-and-times"
    xmlns:col="http://conserveonline.org/namespaces/col" extension-element-prefixes="date col"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="calendarmonthview.xsl"/>
    <xsl:param name="staticprefix">/static/</xsl:param>
    <xsl:output indent="yes"/>
    <xsl:template match="view[@name='monthly.html' and @type='calendar']">
        <xsl:call-template name="calendar"/>
    </xsl:template>
    <xsl:template match="event" mode="calendarlisting">
        <xsl:param name="currday"/>
        <xsl:if test="position() = 1">
            <a name="{$currday}"/>
            <dt>
                <xsl:choose>
                    <!-- matched on startDate -->
                    <xsl:when test="$currday = date:day-in-month(startDate)">
                        <xsl:value-of select="date:day-name(startDate)"/>, </xsl:when>
                    <!-- matched on endDate -->
                    <xsl:when test="$currday = date:day-in-month(endDate)">
                        <xsl:value-of select="date:day-name(endDate)"/>, </xsl:when>
                    <!-- calculate date from offset of startdate (somewhere in the middle of startdate and enddate) -->
                    <xsl:otherwise>
                        <xsl:variable name="offset" select="$currday - date:day-in-month(startDate)"/>
                        <xsl:value-of
                            select="date:day-name(date:add(startDate,concat('P',$offset,'D')))"/>,
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:value-of select="$currday"/>
            </dt>
        </xsl:if>
        <dd>
            <xsl:if test="position() mod 2 != 1">
                <xsl:attribute name="class">even</xsl:attribute>
            </xsl:if>
            <a href="{@href}">
                <xsl:value-of select="title"/>
            </a>
        </dd>
    </xsl:template>

    <days xmlns="http://conserveonline.org/namespaces/col">
        <i>1</i>
        <i>2</i>
        <i>3</i>
        <i>4</i>
        <i>5</i>
        <i>6</i>
        <i>7</i>
        <i>8</i>
        <i>9</i>
        <i>10</i>
        <i>11</i>
        <i>12</i>
        <i>13</i>
        <i>14</i>
        <i>15</i>
        <i>16</i>
        <i>17</i>
        <i>18</i>
        <i>19</i>
        <i>20</i>
        <i>21</i>
        <i>22</i>
        <i>23</i>
        <i>24</i>
        <i>25</i>
        <i>26</i>
        <i>27</i>
        <i>28</i>
        <i>29</i>
        <i>30</i>
        <i>31</i>
    </days>

    <xsl:template match="view[@name='listing.html' and @type='calendar']">
        <xsl:variable name="currentDate" select="/response/calendar/@current"/>
        <xsl:variable name="year" select="date:year($currentDate)"/>
        <xsl:variable name="monthName" select="date:month-name($currentDate)"/>

        <xsl:apply-templates select="/response/calendar/navigation"/>

        <dl class="eventsListing">
            <xsl:variable name="possibledays" select="document('')/xsl:stylesheet/col:days/col:i"/>
            <xsl:variable name="resources" select="../calendar/events/event"/>

            <xsl:for-each select="$possibledays">
                <xsl:apply-templates
                    select="$resources[current()>=date:day-in-month(startDate) and current()&lt;=date:day-in-month(endDate)]"
                    mode="calendarlisting">

                    <xsl:with-param name="currday">
                        <xsl:value-of select="."/>
                    </xsl:with-param>
                </xsl:apply-templates>
            </xsl:for-each>
        </dl>
    </xsl:template>


    <!-- Calendar widget for forms -->
    <xsl:template match="@widget[.='calendar']">
        <xsl:variable name="fieldvalue" select="../value"/>
        <xsl:variable name="name" select="../@name"/>

        <xsl:variable name="currentDate">
            <xsl:choose>
                <xsl:when test="$fieldvalue">
                    <xsl:value-of select="$fieldvalue"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:variable name="date" select="date:date-time()"/>
                    <xsl:value-of
                        select="concat(substring-before($date, 'T'), ' ', substring(substring-before(substring-after($date, 'T'), '+'), 1, 5))"
                    />
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <xsl:variable name="currentYear">
            <xsl:choose>
                <xsl:when test="$fieldvalue">
                    <xsl:value-of select="substring($fieldvalue, 1, 4)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="date:year()"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <xsl:variable name="currentMonth">
            <xsl:choose>
                <xsl:when test="$fieldvalue">
                    <xsl:value-of select="substring($fieldvalue, 6, 2)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="date:month-in-year()"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <xsl:variable name="currentDay">
            <xsl:choose>
                <xsl:when test="$fieldvalue">
                    <xsl:value-of select="substring($fieldvalue, 9, 2)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="date:day-in-month()"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <xsl:variable name="currentHour">
            <xsl:choose>
                <xsl:when test="$fieldvalue">
                    <xsl:value-of select="substring($fieldvalue, 12, 2)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="date:hour-in-day()"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <xsl:variable name="currentMinute">
            <xsl:choose>
                <xsl:when test="$fieldvalue">
                    <xsl:value-of select="substring($fieldvalue, 15, 2)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="date:minute-in-hour()"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div id="fieldType" style="display:none">
            <xsl:value-of select="../@name"/>
        </div>

        <div id="{$name}-wrapper">
            <input type="text" size="30" name="{$name}" id="{$name}" value="{$currentDate}"
                readonly="readonly" class="invisible"/>
            <select name="{$name}-year" id="{$name}-year" size="1"
                onchange="updateField('{$name}', '{$name}-year', '{$name}-month', '{$name}-day', '{$name}-hour', '{$name}-minute', '{$name}-ampm')">
                <option value=""/>
                <option value="2003">2003</option>
                <option value="2004">2004</option>
                <option value="2005">2005</option>
                <option value="2006">2006</option>
                <option value="2007">2007</option>
                <option value="2008">2008</option>
                <option value="2009">2009</option>
                <option value="2010">2010</option>
                <option value="2011">2011</option>
                <option value="2012">2012</option>
                <option value="2013">2013</option>
                <option value="2014">2014</option>
                <option value="2015">2015</option>
                <option value="2016">2016</option>
                <option value="2017">2017</option>
                <option value="2018">2018</option>
                <option value="2019">2019</option>
                <option value="2020">2020</option>
                <option value="2021">2021</option>
                <option value="2022">2022</option>
                <option value="2023">2023</option>
            </select>
            <select name="{$name}-month" size="1" id="{$name}-month"
                onchange="updateField('{$name}', '{$name}-year', '{$name}-month', '{$name}-day', '{$name}-hour', '{$name}-minute', '{$name}-ampm')">
                <option value=""/>
                <option value="01">January</option>
                <option value="02">February</option>
                <option value="03">March</option>
                <option value="04">April</option>
                <option value="05">May</option>
                <option value="06">June</option>
                <option value="07">July</option>
                <option value="08">August</option>
                <option value="09">September</option>
                <option value="10">October</option>
                <option value="11">November</option>
                <option value="12">December</option>
            </select>
            <select name="{$name}-day" size="1" id="{$name}-day"
                onchange="updateField('{$name}', '{$name}-year', '{$name}-month', '{$name}-day', '{$name}-hour', '{$name}-minute', '{$name}-ampm')">
                <option value=""/>
                <option value="01">01</option>
                <option value="02">02</option>
                <option value="03">03</option>
                <option value="04">04</option>
                <option value="05">05</option>
                <option value="06">06</option>
                <option value="07">07</option>
                <option value="08">08</option>
                <option value="09">09</option>
                <option value="10">10</option>
                <option value="11">11</option>
                <option value="12">12</option>
                <option value="13">13</option>
                <option value="14">14</option>
                <option value="15">15</option>
                <option value="16">16</option>
                <option value="17">17</option>
                <option value="18">18</option>
                <option value="19">19</option>
                <option value="20">20</option>
                <option value="21">21</option>
                <option value="22">22</option>
                <option value="23">23</option>
                <option value="24">24</option>
                <option value="25">25</option>
                <option value="26">26</option>
                <option value="27">27</option>
                <option value="28">28</option>
                <option value="29">29</option>
                <option value="30">30</option>
                <option value="31">31</option>
            </select>

            <img src="{$staticprefix}images/img.gif" id="trigger-{$name}" class="calendarTrigger"
                title="Date selector" onmouseover="this.style.background='red';"
                onmouseout="this.style.background=''" alt=""/>
            <span>
                <xsl:if test="../@name = 'form.dateauthored'">
                    <xsl:attribute name="style">display:none</xsl:attribute>
                </xsl:if>
                <select name="{$name}-hour" size="1" id="{$name}-hour"
                    onchange="updateField('{$name}', '{$name}-year', '{$name}-month', '{$name}-day', '{$name}-hour', '{$name}-minute', '{$name}-ampm')">
                    <option value="00">01</option>
                    <option value="01">02</option>
                    <option value="02">03</option>
                    <option value="03">04</option>
                    <option value="04">05</option>
                    <option value="05">06</option>
                    <option value="06">07</option>
                    <option value="07">08</option>
                    <option value="08">09</option>
                    <option value="09">10</option>
                    <option value="10">11</option>
                    <option value="11">12</option>
                </select> : <select name="{$name}-minute" size="1" id="{$name}-minute"
                    onchange="updateField('{$name}', '{$name}-year', '{$name}-month', '{$name}-day', '{$name}-hour', '{$name}-minute', '{$name}-ampm')">
                    <option value="00">00</option>
                    <option value="01">01</option>
                    <option value="02">02</option>
                    <option value="03">03</option>
                    <option value="04">04</option>
                    <option value="05">05</option>
                    <option value="06">06</option>
                    <option value="07">07</option>
                    <option value="08">08</option>
                    <option value="09">09</option>
                    <option value="10">10</option>
                    <option value="11">11</option>
                    <option value="12">12</option>
                    <option value="13">13</option>
                    <option value="14">14</option>
                    <option value="15">15</option>
                    <option value="16">16</option>
                    <option value="17">17</option>
                    <option value="18">18</option>
                    <option value="19">19</option>
                    <option value="20">20</option>
                    <option value="21">21</option>
                    <option value="22">22</option>
                    <option value="23">23</option>
                    <option value="24">24</option>
                    <option value="25">25</option>
                    <option value="26">26</option>
                    <option value="27">27</option>
                    <option value="28">28</option>
                    <option value="29">29</option>
                    <option value="30">30</option>
                    <option value="31">31</option>
                    <option value="32">32</option>
                    <option value="33">33</option>
                    <option value="34">34</option>
                    <option value="35">35</option>
                    <option value="36">36</option>
                    <option value="37">37</option>
                    <option value="38">38</option>
                    <option value="39">39</option>
                    <option value="40">40</option>
                    <option value="41">41</option>
                    <option value="42">42</option>
                    <option value="43">43</option>
                    <option value="44">44</option>
                    <option value="45">45</option>
                    <option value="46">46</option>
                    <option value="47">47</option>
                    <option value="48">48</option>
                    <option value="49">49</option>
                    <option value="50">50</option>
                    <option value="51">51</option>
                    <option value="52">52</option>
                    <option value="53">53</option>
                    <option value="54">54</option>
                    <option value="55">55</option>
                    <option value="56">56</option>
                    <option value="57">57</option>
                    <option value="58">58</option>
                    <option value="59">59</option>
                </select>
                <select name="{$name}-ampm" size="1" id="{$name}-ampm"
                    onchange="updateField('{$name}', '{$name}-year', '{$name}-month', '{$name}-day', '{$name}-hour', '{$name}-minute', '{$name}-ampm')">
                    <option value="1">AM</option>
                    <option value="2">PM</option>
                </select>
            </span>
            <div style="display:none">
                <xsl:attribute name="class">DateVal-<xsl:value-of select="$name"/></xsl:attribute>
                <xsl:variable name="CalendarInitVal2">
                    <xsl:value-of select="$name"/>::<xsl:value-of select="$currentYear"
                        />::<xsl:value-of select="$currentMonth"/>::<xsl:value-of
                        select="$currentDay"/>::<xsl:value-of select="$currentHour"/>::<xsl:value-of
                        select="$currentMinute"/>
                </xsl:variable>
                <xsl:value-of select="$CalendarInitVal2"/>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="view[@name='view.html' and @type='event']">
        <div class="contentWrapper">

            <dl id="event-view-listing">
                <dt>Event Starts</dt>
                <dd>
                    <xsl:apply-templates select="/response/resource/startDate" mode="bloglongform"/>
                </dd>

                <dt>Event Ends</dt>
                <dd>
                    <xsl:apply-templates select="/response/resource/endDate" mode="bloglongform"/>
                </dd>

                <dt>Body</dt>
                <dd>
                    <div class="kbody">
                        <xsl:apply-templates select="/response/resource/text/*" mode="copy"/>
                    </div>
                </dd>

                <xsl:if test="/response/resource/location">
                    <dt>Location</dt>
                    <dd>
                        <xsl:value-of select="/response/resource/location"/>
                    </dd>
                </xsl:if>

                <xsl:if test="/response/resource/contactName">
                    <dt>Contact</dt>
                    <dd>
                        <xsl:value-of select="/response/resource/contactName"/>
                    </dd>
                </xsl:if>

                <xsl:if test="/response/resource/contactName">
                    <dt>Contact Email</dt>
                    <dd>
                        <a href="mailto:{/response/resource/contactEmail}"
                            title="Mail to {/response/resource/contactName}">
                            <xsl:value-of select="/response/resource/contactEmail"/>
                        </a>
                    </dd>
                </xsl:if>

                <xsl:if test="/response/resource/attendees">
                    <dt>Attendees</dt>
                    <dd>
                            <xsl:for-each select="/response/resource/attendees/item">
                                <span>
                                    <xsl:value-of select="."/>
                                    <xsl:choose>
                                        <xsl:when test="position() = last()">.</xsl:when>
                                        <xsl:otherwise>,&#160;</xsl:otherwise>
                                    </xsl:choose>
                                    
                                </span>
                            </xsl:for-each>
                    </dd>
                </xsl:if>

                <xsl:if test="/response/resource/attachments/attachment">
                    <dt>Attachment</dt>
                    <dd>
                        <a href="{/response/resource/attachments/attachment/@href}">
                            <xsl:value-of select="/response/resource/attachments/attachment"/>
                        </a>
                    </dd>
                </xsl:if>
            </dl>
            <a href="{/response/resource/@href}/vcs_view" title="Save To Outlook"
                style="display: block; margin-top: 1em; color: #639332">
                <strong>Save To Outlook</strong>
            </a>
        </div>
    </xsl:template>

</xsl:stylesheet>
