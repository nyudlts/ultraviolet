from ultraviolet.policies import UltraVioletPermissionPolicy


def outcomes(identity, records, requested, outcome):
    return {
        group: {
            action
            for action in actions
            if UltraVioletPermissionPolicy(action, record=records[group]).allows(
                identity
            )
            is outcome
        }
        for group, actions in requested.items()
    }


def allowed(identity, records, requested):
    return outcomes(identity, records, requested, outcome=True)


def denied(identity, records, requested):
    return outcomes(identity, records, requested, outcome=False)
