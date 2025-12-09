using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class CacheDeletionRequest
    {
        public string ConversationIdState;
        public string ConversationIdTemplate;
        
        public CacheDeletionRequest() { }
        public class Builder
        {
            private CacheDeletionRequest _build = new CacheDeletionRequest();
            public Builder ConversationIdState(string conversationIdState) { 
                _build.ConversationIdState = conversationIdState; 
                return this;
            }
            public Builder ConversationIdTemplate(string conversationIdTemplate) { 
                _build.ConversationIdTemplate = conversationIdTemplate; 
                return this;
            }
            public CacheDeletionRequest Build()
            {
                return _build;
            }
        }
    }
}