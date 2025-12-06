using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class CacheDeletionRequest
    {
        public string ConversationId;
        
        public CacheDeletionRequest() { }
        public class Builder
        {
            private CacheDeletionRequest _build = new CacheDeletionRequest();
            public Builder ConversationId(string conversationId) { 
                _build.ConversationId = conversationId; 
                return this;
            }
            public CacheDeletionRequest Build()
            {
                return _build;
            }
        }
    }
}