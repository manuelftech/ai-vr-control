def get_formatted_vr_state(template):
    print(f"[Validation] Received template: {template}")
    """```
    Query:
    @Tag:{cube} 
    @ComponentColor:{\#808080}
    @ComponentConstantForceY:[]

    Properties:
    $.Components.Color = #00FF00
    $.Components.ConstantForce.Y = 9.83
    ```"""
    return template["template"]