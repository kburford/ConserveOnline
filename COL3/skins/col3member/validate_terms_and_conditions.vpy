## Script (Python) "validate_terms_and_conditions"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=license_agree=None
##title=checks if user agreed to Terms and Conditions
##
if not license_agree:
    state.setError('license_agree', "You cannot proceed if you don't agree with these conditions.", 'license_agreement_required')
    state.set(status='failure',
              portal_status_message='Please correct the indicated errors')

return state
