<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">


<html>
<head>
<title>Xpilot-AI Python Interface Reference</title>

<style type="text/css">
body {
	background-color: #F8F8F8;
	color: #000000;
	font-family: arial;
	margin-top:0px;
	margin-left:0px;
	margin-right:0px;
}

a:link { 
	color: #2794BF;
	text-decoration: none;
}
a:visited {
	color: #2289B2;
	text-decoration: none;
}
a:hover {color: #AB4B30}
a:active {color: #AB4B30}

div.main_reference
{
	margin-left: 25px;
	margin-right: 20%;
	margin-top: 25px;
}

div.category
{
	border-left-style: solid;
	border-left-width: 10px;
	border-left-color: #FFC39D;
}

div.category_name
{
	background-color: #DBF0FF;
	color: #000000;
	font-weight: bold;
}
div.category_desc
{
	padding-left: 25px;
	background-color: #EEEEEE;
}
div.function
{
	background-color: #FFFFFF;
	margin-top: 25px;
	margin-left: 25px;
	border-width: 0px;
	border-style: solid;
	border-left-width: 1px;
	border-right-width: 1px;
}
div.function_header
{
	background-color: #EEEEEE;
	border-left-style: solid;
	border-left-width: 5px;
	border-top-style: solid;
	border-top-width: 1px;
	border-left-color: #000000;
	padding-left: 15px;
}
span.function_name
{
	color: #000000;
	font-weight: bold;
}
span.function_var_name
{
	color: #2794BF;
}
span.function_return_type
{
	color: #AB4B30;
	font-weight: normal;
}
div.function_var_list
{
	margin-left: 20px;
}
div.function_desc_section
{
	margin-top: 10px;
	margin-left: 20px;
	font-weight: bold;
}
div.function_desc
{
	margin-left: 10px;
	font-weight: normal;
}
div.function_returns
{
	color: #AB4B30;
	margin-top:10px;
	margin-left:20px;
	font-weight: bold;
}
span.function_return_desc
{
	color: black;
	font-weight: normal;
}
span.function_var_desc
{
	color: #555555;
}

div.function_example
{
	margin-left:20px;
	font-weight: bold;
	margin-top:10px;
}
div.function_example_box
{	
	white-space: pre;
	font-family: courier;
	font-weight: normal;
	border-width: 1px;
	border-style: solid;
	background-color: #CCCCCC;
	margin-right:25px;
	overflow:auto;
	font-size: 10pt;
}	

div.function_subnote
{	
	white-space: pre;
	font-family: courier;
	font-weight: normal;
	border-width: 1px;
	border-style: solid;
	background-color: #EEEEEE;
	margin-right:25px;
	margin-left:20px;
	overflow:auto;
	font-size: 10pt;
}
div.function_see_also
{
	border-bottom-width: 1px;
	border-bottom-style: solid;
	margin-top: 10px;
}
span.function_see_also
{
	background-color: #FFC39D;
	margin-right: 5px;
}	
flink
{
	color: #0000FF;
}


div.quick_reference
{
	margin-left: 25px;
	background-color: #FFFFFF;
	margin-right: 20%;
}

span.qcategory_name
{
	background-color: #DBF0FF;
	color: #000000;
	font-weight: bold;
	padding-left: 10px;
	padding-right: 10px;
	border-left-style: solid;
	border-left-width: 5px;
	border-left-color: #FFC39D;
}
</style>
</head>

<body>
		<a id="top" />
<h2 style="padding: 10px; padding-left: 25px; background-color: #FFC39D; margin-top: 0px;">Xpilot-AI Python Interface Reference</h2>
	<div class="quick_reference">
	<xsl:for-each select="header/category">
		
		<span class="qcategory_name"><xsl:value-of select="name" /></span><br />

		<xsl:for-each select="function">
			<div class="qfunction_header">
			<a style="color: black;"><xsl:attribute name="href">#<xsl:value-of select="name"/></xsl:attribute>
			<span class="function_name"><xsl:value-of select="name"/> (</span>
			<xsl:for-each select="input_vars/var">
				<span class="function_var_type">&#160;<xsl:value-of select="type" />&#160;</span>
				<span class="function_var_name"><xsl:value-of select="name" />&#160;</span>
				<xsl:if test="position() &lt; last()">,</xsl:if>
			</xsl:for-each>
			<span class="function_name">)</span></a> <img src="arrow.png" style="padding-right: 8px; padding-left: 8px;"/>  			
			<span class="function_return_type"><xsl:value-of select="return_var/type"/>&#160;</span>
		</div>
		</xsl:for-each>
		<br />
	</xsl:for-each>	




	</div>

	<div class="main_reference">
	
	<xsl:for-each select="header/category">
		
		<div class="category">
		<div class="category_name"><xsl:value-of select="name" /></div>
		<div class="category_desc"><xsl:value-of select="desc" /></div>
		</div>
		
		<xsl:for-each select="function">
			<a><xsl:attribute name="id"><xsl:value-of select="name"/></xsl:attribute></a>
			<div class="function">
				<div class="function_header"><table style="border-style:none; border-width: 0px; border-spacing:0px; padding:0px; width:100%;"><tr><td>
					<span class="function_return_type"><xsl:value-of select="return_var/type"/>&#160;</span>
					<span class="function_name"><xsl:value-of select="name"/> (</span>
					<xsl:for-each select="input_vars/var">
						<span class="function_var_type">&#160;<xsl:value-of select="type" />&#160;</span>
						<span class="function_var_name"><xsl:value-of select="name" />&#160;</span>
						<xsl:if test="position() &lt; last()">,</xsl:if>
					</xsl:for-each>
					<span class="function_name">)</span></td><td style="text-align: right;">
						<a href="#top">top</a>
					</td></tr></table>
				</div>
				
				<xsl:if test="input_vars/var/type != 'void'">			
				<div class="function_var_list">
					<xsl:for-each select="input_vars/var">
						<span class="function_var_name"><xsl:value-of select="name" />&#160;&#160;</span>
						<span class="function_var_desc"><xsl:value-of select="desc" /></span><br />
					</xsl:for-each>
				</div>
				</xsl:if>
				
				<xsl:if test="desc">
				<div class="function_desc_section">Description:
					<div class="function_desc"><xsl:value-of select="desc"/></div>	
				</div>
				</xsl:if>
				
				<xsl:if test="return_var/desc">
				<div class="function_returns">
				Returns:&#160;&#160;<span class="function_return_desc"><xsl:value-of select="return_var/desc"/></span>
				</div>
				</xsl:if>
				
				<xsl:if test="example">
				<div class="function_example">Example:
				<div class="function_example_box"><xsl:value-of select="example"/></div>
				</div>
				</xsl:if>
				
				<xsl:if test="subnote">
				<div class="function_subnote"><xsl:value-of select="subnote"/></div>
				</xsl:if>
				
				
				<div class="function_see_also"><span class="function_see_also">See Also:&#160;&#160;</span>
					<xsl:for-each select="see_also/flink">
						<a class="function_see_also_flink">
							<xsl:attribute name="href">
								#<xsl:value-of select="."/> 			
							</xsl:attribute>
							<xsl:value-of select="." />
						</a>&#160;&#160;
					</xsl:for-each>				
				</div>
				

			</div>
			
			<br/>
		</xsl:for-each>
		<br />
	</xsl:for-each>

	</div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>


