using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class APIStateRequest
    {
        public string Prompt;
        public string ConversationId;
        
        public APIStateRequest() { }
        public class Builder
        {
            private APIStateRequest _build = new APIStateRequest();
            public Builder Prompt(string prompt) { 
                _build.Prompt = prompt; 
                return this;
            }
            public Builder ConversationId(string conversationId) { 
                _build.ConversationId = conversationId; 
                return this;
            }
            public APIStateRequest Build()
            {
                return _build;
            }
        }
    }
}