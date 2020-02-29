from puppet.templates import pick_first_match
from puppet import coco
from puppet.state import OutOfContext
from puppet.nlu.regex import RegexIntent

from puppet.std.eliza import eliza_fallback

intent_hi = RegexIntent(r"(.*)\b(hi|hello|hey)\b(.*)")
intent_no = RegexIntent(r"(.*)\b(no|nope|never)\b(.*)")
intent_yes = RegexIntent(r"(.*)\b(yes|ok|sure|yup|yea)\b(.*)")

async def sample_bot(state):
    await state.say("Welcome to sample bot")
    user_input = await state.user_input()
    with OutOfContext(state, eliza_fallback):
        await coco(state, "namer_vp3", user_input)
        #await coco(state, "register_vp3")
        await help_line(state)
        await lobby(state)

async def fallback(state):
    await state.say("what?")

async def help_line(state):
    user_input = state.last_user_input()
    await pick_first_match(
        user_input,
        {
            intent_hi: (state.say, "hello back, how can I help")
        },
        (state.say, "How can I help?")
    )

async def lobby(state):
    while True:
        user_input = await state.user_input()
        await pick_first_match(
            user_input,
            {
                RegexIntent(r"(.*)\b(pet)\b(.*)"): (coco, state, "users_pet_vp3", user_input),
                RegexIntent(r"(.*)\b(hobby)\b(.*)"): (coco, state, "user_hobby_vp3", user_input),
            },
            (state.out_of_context,)
        )

if __name__ == "__main__":
    import asyncio
    from puppet.shell import bot_runner
    
    asyncio.run(bot_runner(sample_bot))