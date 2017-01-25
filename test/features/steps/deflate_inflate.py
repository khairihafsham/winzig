from behave import given, when, then
from grab import Grab

deflated_url = None


@given('I want to shorten "{url}"')
def step_want_to_shorten_url(context, url):
    context.url = url
    context.g = Grab()


@when('I submit the URL')
def step_submit_url(context):
    g = context.g
    g.go('localhost:5000')
    g.doc.set_input('url', context.url)
    g.doc.submit()


@then('I should see an error')
def step_see_an_error(context):
    el = context.g.doc.pyquery('div.alert-danger')
    assert len(el)


@then('I should see a new short URL')
def step_see_a_new_short_url(context):
    global deflated_url
    el = context.g.pyquery('input#copyme')
    assert len(el)

    el = el[0]
    assert el.value.startswith('http://')

    deflated_url = el.value


@then('I should see the same short URL')
def step_see_the_same_short_url(context):
    global deflated_url
    el = context.g.pyquery('input#copyme')
    assert len(el)

    el = el[0]
    assert el.value.startswith('http://')
    assert el.value == deflated_url


@given('I want to inflate the previous deflated URL')
def step_want_to_inflate_previous_deflate_url(context):
    global deflated_url
    context.deflated_url = deflated_url
    context.g = Grab()


@when('I go to the deflated URL')
def step_go_to_deflated_url(context):
    context.doc = context.g.go(context.deflated_url)


@then('I should be redirected to "{url}"')
def step_should_be_redirected_to(context, url):
    assert url in context.doc.url
