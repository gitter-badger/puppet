from puppet.state import Outputs
from coco.async_api import ComponentSession


async def coco(state, component_id, user_input=None, context={}, **params):
    component_session = ComponentSession(component_id, state.session_id)

    if not user_input:
        user_input = await state.user_input()

    component_response = await component_session(
        user_input, context=context, parameters=params
    )
    while not component_response.component_done:
        if component_response.response:
            await state.say(component_response.response)
        state.memory = {**state.memory, **component_response.updated_context}
        if component_response.out_of_context:
            await state.out_of_context(state.last_user_input())
        user_input = await state.user_input()
        component_response = await component_session(
            user_input, context=context, parameters=params
        )

    if component_response.response:
        await state.say(component_response.response)
    if component_response.component_failed:
        return Outputs(success=False)
