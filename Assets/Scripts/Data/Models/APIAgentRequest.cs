using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class APIAgentRequest
    {
        public string Prompt;
        public string ConversationId;
        
        public APIAgentRequest() { }
        public class Builder
        {
            private APIAgentRequest _build = new APIAgentRequest();
            public Builder Prompt(string prompt) { 
                _build.Prompt = prompt; 
                return this;
            }
            public Builder ConversationId(string conversationId) { 
                _build.ConversationId = conversationId; 
                return this;
            }
            public APIAgentRequest Build()
            {
                return _build;
            }
        }
    }
}