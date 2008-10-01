<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:date="http://exslt.org/dates-and-times" extension-element-prefixes="date"
  xmlns="http://www.w3.org/1999/xhtml" version="1.0">
  <xsl:import href="date.add.template.xsl"/>
  <xsl:template match="/">
    <xsl:call-template name="calendar"/>
  </xsl:template>

  <xsl:template name="calendar">
    <xsl:variable name="currentDate" select="/response/calendar/@current"/>

    <!-- Calculate the offset to the first day in this month -->
    <xsl:variable name="first-day-offset">
      <xsl:text>-P</xsl:text>
      <xsl:value-of select="date:day-in-month($currentDate) - 1"/>
      <xsl:text>D</xsl:text>
    </xsl:variable>

    <!-- XXX Replacing add function with call to add template XXX-->
    <xsl:variable name="first-of-month">
      <xsl:call-template name="date:add">
        <xsl:with-param name="date-time" select="$currentDate"/>
        <xsl:with-param name="duration" select="$first-day-offset"/>
      </xsl:call-template>
    </xsl:variable>
    <!-- Calculate the offset to the first Sunday before or on the
      first of this month -->

    <xsl:variable name="first-sunday-offset">
      <xsl:text>-P</xsl:text>
      <xsl:value-of select="date:day-in-week($first-of-month) - 1"/>
      <xsl:text>D</xsl:text>
    </xsl:variable>
    <xsl:variable name="start-of-calendar">
      <xsl:call-template name="date:add">
        <xsl:with-param name="date-time" select="$first-of-month"/>
        <xsl:with-param name="duration" select="$first-sunday-offset"/>
      </xsl:call-template>
    </xsl:variable>

    <xsl:apply-templates select="/response/calendar/calendarlinks"/>

    <table id="cal" summary="Calendar for {date:month-name($currentDate)} {date:year($currentDate)}">

      <thead>
        <tr class="calendar_day_of_week_header">
          <th>Sun</th>
          <th>Mon</th>
          <th>Tues</th>
          <th>Wed</th>
          <th>Thurs</th>
          <th>Fri</th>
          <th>Sat</th>
        </tr>
      </thead>

      <!-- Call the template with two parameters: where to start and
        when to end -->

      <xsl:call-template name="calendar-week">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="start-date" select="$start-of-calendar"/>
        <xsl:with-param name="for-month" select="date:month-in-year($currentDate)"/>
      </xsl:call-template>
    </table>
  </xsl:template>

  <xsl:template name="calendar-week">
    <xsl:param name="currentDate"/>
    <xsl:param name="start-date"/>
    <xsl:param name="for-month"/>

    <tr>
      <xsl:call-template name="calendar-day">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="day" select="$start-date"/>
        <xsl:with-param name="for-month" select="$for-month"/>
      </xsl:call-template>
      <xsl:variable name="daytwo">
        <xsl:call-template name="date:add">
          <xsl:with-param name="date-time" select="$start-date"/>
          <xsl:with-param name="duration" select="'P1D'"/>
        </xsl:call-template>
      </xsl:variable>
      <xsl:call-template name="calendar-day">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="day" select="$daytwo"/>
        <xsl:with-param name="for-month" select="$for-month"/>
      </xsl:call-template>
      <xsl:variable name="daythree">
        <xsl:call-template name="date:add">
          <xsl:with-param name="date-time" select="$start-date"/>
          <xsl:with-param name="duration" select="'P2D'"/>
        </xsl:call-template>
      </xsl:variable>
      <xsl:call-template name="calendar-day">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="day" select="$daythree"/>
        <xsl:with-param name="for-month" select="$for-month"/>
      </xsl:call-template>
      <xsl:variable name="dayfour">
        <xsl:call-template name="date:add">
          <xsl:with-param name="date-time" select="$start-date"/>
          <xsl:with-param name="duration" select="'P3D'"/>
        </xsl:call-template>
      </xsl:variable>
      <xsl:call-template name="calendar-day">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="day" select="$dayfour"/>
        <xsl:with-param name="for-month" select="$for-month"/>
      </xsl:call-template>
      <xsl:variable name="dayfive">
        <xsl:call-template name="date:add">
          <xsl:with-param name="date-time" select="$start-date"/>
          <xsl:with-param name="duration" select="'P4D'"/>
        </xsl:call-template>
      </xsl:variable>
      <xsl:call-template name="calendar-day">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="day" select="$dayfive"/>
        <xsl:with-param name="for-month" select="$for-month"/>
      </xsl:call-template>
      <xsl:variable name="daysix">
        <xsl:call-template name="date:add">
          <xsl:with-param name="date-time" select="$start-date"/>
          <xsl:with-param name="duration" select="'P5D'"/>
        </xsl:call-template>
      </xsl:variable>
      <xsl:call-template name="calendar-day">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="day" select="$daysix"/>
        <xsl:with-param name="for-month" select="$for-month"/>
      </xsl:call-template>
      <xsl:variable name="dayseven">
        <xsl:call-template name="date:add">
          <xsl:with-param name="date-time" select="$start-date"/>
          <xsl:with-param name="duration" select="'P6D'"/>
        </xsl:call-template>
      </xsl:variable>
      <xsl:call-template name="calendar-day">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="day" select="$dayseven"/>
        <xsl:with-param name="for-month" select="$for-month"/>
      </xsl:call-template>
    </tr>

    <xsl:variable name="next-week">
      <xsl:call-template name="date:add">
        <xsl:with-param name="date-time" select="$start-date"/>
        <xsl:with-param name="duration" select="'P7D'"/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:if test="$for-month = date:month-in-year($next-week)">
      <xsl:call-template name="calendar-week">
        <xsl:with-param name="currentDate" select="$currentDate"/>
        <xsl:with-param name="start-date" select="$next-week"/>
        <xsl:with-param name="for-month" select="$for-month"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template name="calendar-day">
    <xsl:param name="currentDate"/>
    <xsl:param name="day"/>
    <xsl:param name="for-month"/>

    <td height="90" width="90" valign="top">
      <xsl:attribute name="class">
        <xsl:choose>
          <xsl:when test="$for-month != date:month-in-year($day)">
            <xsl:text>other-month</xsl:text>
          </xsl:when>
          <xsl:when test="$currentDate = $day and $for-month = date:month-in-year()">
            <xsl:text>this-day</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text>this-month</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:attribute>

      <!-- First we need to get the events that have started before or in our current date -->
      <xsl:variable name="prevevents"
        select="/response/calendar/events/event[date:day-in-year(startDate) &lt;= date:day-in-year($day)]"/>

      <!-- Now we get the events that has to end in or after our current date -->
      <xsl:variable name="todaysevents"
        select="$prevevents[date:day-in-year(endDate) >= date:day-in-year($day)]"/>

      <xsl:choose>
        <!-- 
          First choose whether to wrap the day in a link to the day page.  If there 
          are no events for that day, display it with no <a>.
        -->
        <xsl:when test="count($todaysevents)">
          <a
            href="{/response/workspace/@href}/calendar/listing.html#{date:day-in-month($day)}">
            <span class="calendar_day_header" style="display: block">
              <xsl:value-of select="date:day-in-month($day)"/>
            </span>
          </a>
        </xsl:when>
        <xsl:otherwise>
          <xsl:if test="$for-month != date:month-in-year($day)">  
            <div class="calendar_day_header_inactive">
              <xsl:value-of select="date:day-in-month($day)"/>
            </div>
          </xsl:if>
          <xsl:if test="$for-month = date:month-in-year($day)">
       
            <div class="calendar_day_header">
              <xsl:value-of select="date:day-in-month($day)"/>
            </div>

          </xsl:if>
        </xsl:otherwise>
      </xsl:choose>
      
      <xsl:for-each select="$todaysevents[position() &lt; 3]">
        <div style="padding: 3px; color: #999"> &#8226;<a href="{@href}" title="{title}">
            <xsl:value-of select="substring(title,1,20)"/>
            <xsl:if test="string-length(title) &gt; 21">...</xsl:if>
          </a>
        </div>
      </xsl:for-each>
      <xsl:if test="count($todaysevents) &gt; 2">
        <div style="padding: 3px; text-align:left;">
          <a
            href="{/response/community/@href}/calendar/listing.html#{date:day-in-month($day)}"
              >+<xsl:value-of select="count($todaysevents) - 2"/> more</a>
        </div>
      </xsl:if>
  <div style="padding:6px;color:#eeeeee; text-align:right;font-size:9px">
    <a style="text-decoration:none;" alt="Add Event" title="Add Event" href="{/response/workspace/@href}/calendar/@@add-event.html?ymd={date:date($day)}">( + )</a>
  </div>
    </td>
  </xsl:template>
  <xsl:template match="calendar/navigation">
    <div class="batchNavigation">
      
      <xsl:if test="previous">
        <span class="previousMonth">
          <a href="" title="">
            <xsl:attribute name="href">
              <xsl:value-of select="previous/@href"/>              
            </xsl:attribute>
            &#x25C0;
            <xsl:value-of select="date:month-name(previous)"/>
            <xsl:text> </xsl:text>
            <xsl:value-of select="date:year(previous)"/>
            </a>
        </span>
      </xsl:if>
      
      <xsl:if test="previous and next">
        |
      </xsl:if>
      
      <xsl:if test="next">
        <span class="nextMonth">
          <a href="" title="">
            <xsl:attribute name="href">
              <xsl:value-of select="next/@href"/>              
            </xsl:attribute>
            <!--<xsl:value-of select="next"/>-->
            <xsl:value-of select="date:month-name(next)"/>
            <xsl:text> </xsl:text>
            <xsl:value-of select="date:year(next)"/>
            &#x25B6;
          </a>
        </span>
      </xsl:if>
      
    </div>
  </xsl:template>
  

  
  <xsl:template match="calendar/calendarlinks">
    <p align="center">
      <a  href="{prevyearlink/@href}">
        <xsl:value-of select="prevyearlink"/>
      </a> |
      <xsl:for-each select="calendarlink">
        <xsl:choose>
          <xsl:when test="@current">
            <span class="alpha-menu-select">
              <xsl:value-of select="."/>
            </span>
          </xsl:when>
          <xsl:otherwise>
            <a  href="{@href}">
              <xsl:value-of select="."/>
            </a>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="position() != last()"> | </xsl:if>
      </xsl:for-each>
      | <a  href="{nextyearlink/@href}">
        <xsl:value-of select="nextyearlink"/>
      </a> 
    </p>
  </xsl:template>

</xsl:stylesheet>
