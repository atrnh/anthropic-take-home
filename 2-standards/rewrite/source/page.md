# Install a plugin

Add a plugin in Claude Desktop to extend what Claude can do in Cowork and Code. A
plugin packages capabilities such as skills, commands, connectors, and hooks so you
can install them together. The [plugins overview](https://claude.com/docs/plugins/overview)
explains how plugins work across Claude products. To install plugins in the Claude
Code CLI, see [Discover and install prebuilt plugins](https://code.claude.com/docs/en/discover-plugins).

The steps depend on how you get access to Claude. Choose the guide that matches
the Claude account you are using for this task.

<div class="chooser" hidden>
<label for="instructions">Instructions for</label>
<select id="instructions" data-default="{{ default_variant | e }}">
  <option value="">Choose a guide</option>
{% for variant in variants %}
  <option value="{{ variant.id | e }}"{% if variant.default %} selected{% endif %}>{{ variant.label | e }}</option>
{% endfor %}
  <option value="all">Show all guides</option>
</select>
<p id="selection-status" role="status" aria-live="polite"></p>
</div>

<details class="help" markdown="1">
<summary><h2 id="which-guide-should-i-use">Which guide should I use?</h2></summary>

If your organization provides Claude for Government, use the
**Claude Desktop (Government)** guide.

Otherwise, if you use Claude on your own or through a Team or Enterprise plan,
use the **Claude Desktop (General)** guide.

If you are not sure which applies, ask your administrator or the person who
manages Claude:

> Which plugin installation guide applies to my Claude account: Claude Desktop
> (General), Claude Desktop (Government), or another setup?

You can also choose **Show all guides** to compare the instructions.
If neither guide matches your setup, ask that person for the relevant instructions.
</details>

{% for variant in variants %}
<div id="{{ variant.id | e }}" class="variant" markdown="1">

<h2 id="{{ variant.id | e }}-heading">{{ variant.label | e }}</h2>

{{ variant.content }}

</div>
{% endfor %}
