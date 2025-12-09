using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class ConversationStateResponse
    {
        public string ConversationIdState;
        public string ConversationIdTemplate;
        
        public ConversationStateResponse() { }
        public class Builder
        {
            private ConversationStateResponse _build = new ConversationStateResponse();
            public Builder ConversationIdState(string conversationIdState)
            {
                 _build.ConversationIdState = conversationIdState;
                 return this;
            }
            public Builder ConversationIdTemplate(string conversationIdTemplate)
            {
                 _build.ConversationIdTemplate = conversationIdTemplate;
                 return this;
            }
            public ConversationStateResponse Build()
            {
                return _build;
            }
        }
    }
}