
Open Questions
==========================


Closed Questions
==================

- Move <required/> to an attribute

- There is a viewids.rng that manages the list of allowed view ids.

- We should never see <foo>  </foo>.

- If something doesn't have a value, omit the element (so we can make
  better XPath rules).

- For now, subelement order matters.

- Field names have "form.fieldname" as their name

- I'm using a:documentation to bake in the "why" and also to improve
  the process of editing sampledata by hand.

- Use @href when you are pointing to the canonical URL for something.
  In RDF terms, something like this::

  <portlet id="recent-items">
    <item href="/some/other/item">Title of Document</item>

...means portlet is the subject, item is the predicate, and
some-other-item is the object.
