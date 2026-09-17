# Install a plugin

Add a plugin to extend what Claude can do in Cowork and Code. A
[plugin](https://claude.com/docs/plugins/overview) packages capabilities such as skills,
commands, and other tools so you can install them together.

The available plugins and installation behavior depend on how your organization
provides Claude. Choose the guide that matches the Claude account you are using
for this task.

<div class="help" markdown="1">
## Which guide should I use?

If you are using Claude as an individual, start with the **Claude Desktop (General)**
guide.

If you access Claude through an organization that is using Claude for Government, select
the **Claude Desktop (Government)** guide. If you are not sure, ask your administrator or
the person who manages Claude:

> Which plugin installation guide applies to my Claude account: the general
> Cowork guide, Claude for Government, or another setup?

You can also choose **Show all guides** to compare the instructions.
If neither guide matches your setup, ask that person for the relevant instructions.
</div>

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

{% for variant in variants %}
<div id="{{ variant.id | e }}" class="variant" markdown="1">

<h2 id="{{ variant.id | e }}-heading">{{ variant.label | e }}</h2>

{{ variant.content }}

</div>
{% endfor %}
