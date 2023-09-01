# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *


def save_context(context):
    # save context to file .
    import pickle
    with open("context.pkl", "wb") as f:
        pickle.dump(context, f)


@plugins.register(
    name="Login",
    desire_priority=-1,
    hidden=True,
    desc="A simple plugin that says login",
    version="0.1",
    author="lanvent",
)
class Login(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Login] inited")

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT,
            ContextType.JOIN_GROUP,
            ContextType.PATPAT,
        ]:
            return

        # save e_context["context"] data to file..

        content = e_context["context"].content
        logger.debug("[Login] on_handle_context. content: %s" % content)
        if content == "Login":
            reply = Reply()
            reply.type = ReplyType.TEXT
            msg: ChatMessage = e_context["context"]["msg"]
            if e_context["context"]["isgroup"]:
                reply.content = f"Register this group succ by {msg.from_user_nickname}"
                save_context(context= e_context["context"])
            else:
                reply.content = f"Can't support single chat ."
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

    def get_help_text(self, **kwargs):
        help_text = "会把当前群组的上下文记录下来, 给之后的Send使用"
        return help_text
