using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class ConversationStateResponse
    {
        public string ConversationId;
        
        public ConversationStateResponse() { }
        public class Builder
        {
            private ConversationStateResponse _build = new ConversationStateResponse();
            public Builder ConversationId(string conversationId)
            {
                 _build.ConversationId = conversationId;
                 return this;
            }
            public ConversationStateResponse Build()
            {
                return _build;
            }
        }
    }
}