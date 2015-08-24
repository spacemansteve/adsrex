from ..user_roles import anonymous_user, authenticated_user, bumblebee_user

bibcode = '1995ApJ...447L..37W'

def test_anonymous_user():
    # Try to get graphics info for an existing bibcode
    r = anonymous_user.get('/graphics/%s'%bibcode)
    # We should get a 401 back
    assert r.status_code == 401
    # The same for a non-existing bibcode
    r = anonymous_user.get('/graphics/foo')
    # We should get a 401 back
    assert r.status_code == 401

def test_authenticated_user():
    # Get graphics for an existing bibcode
    r = authenticated_user.get('/graphics/%s'%bibcode)
    # We should get a 200 back
    assert r.status_code == 200
    # Now we'll test the contents of what was sent back
    data = r.json()
    # The data structure sent back has a 'bibcode' entry,
    # which should contain the request bibcode
    assert data['bibcode'] == bibcode
    # and the 'eprint' attribute should say False
    assert data['eprint'] == False
    # The attribute 'figures' should be a list
    assert isinstance(data['figures'], list)
    # The list of figures should not be empty
    assert len(data['figures']) > 0
    # A figure in the list of figures should have expected attributes
    expected_attr = [u'images', u'figure_caption', u'figure_label', u'figure_id']
    assert sorted(data['figures'][0].keys()) == sorted(expected_attr)
    # The attribute 'images' refers to a list
    assert isinstance(data['figures'][0]['images'], list)
    # The list of images should not be empty
    assert len(data['figures'][0]['images']) > 0
    # The list of images should contain dictionaries
    # with expected attributes
    im_attr = [u'image_id', u'format', u'thumbnail', u'highres']
    for im in data['figures'][0]['images']:
        assert isinstance(im, dict)
        assert sorted(im.keys()) == sorted(im_attr)
    # A non-existing bibcode should still return a 200
    r = authenticated_user.get('/graphics/foo')
    assert r.status_code == 200
    # But the data structure sent back should have an 'Error' attribute
    assert 'Error' in r.json()

def test_bumblebee_user():
    # The Bumblebee User should be able to access graphics too
    # Get graphics for an existing bibcode
    r = bumblebee_user.get('/graphics/%s'%bibcode)
    # We should get a 200 back
    assert r.status_code == 200
    # We'll do the same tests as for the authenticated user, just to
    # be sure
    data = r.json()
    # The data structure sent back has a 'bibcode' entry,
    # which should contain the request bibcode
    assert data['bibcode'] == bibcode
    # and the 'eprint' attribute should say False
    assert data['eprint'] == False
    # The attribute 'figures' should be a list
    assert isinstance(data['figures'], list)
    # The list of figures should not be empty
    assert len(data['figures']) > 0
    # A figure in the list of figures should have expected attributes
    expected_attr = [u'images', u'figure_caption', u'figure_label', u'figure_id']
    assert sorted(data['figures'][0].keys()) == sorted(expected_attr)
    # The attribute 'images' refers to a list
    assert isinstance(data['figures'][0]['images'], list)
    # The list of images should not be empty
    assert len(data['figures'][0]['images']) > 0
    # The list of images should contain dictionaries
    # with expected attributes
    im_attr = [u'image_id', u'format', u'thumbnail', u'highres']
    for im in data['figures'][0]['images']:
        assert isinstance(im, dict)
        assert sorted(im.keys()) == sorted(im_attr)
    # A non-existing bibcode should still return a 200
    r = bumblebee_user.get('/graphics/foo')
    assert r.status_code == 200
    # But the data structure sent back should have an 'Error' attribute
    assert 'Error' in r.json()
