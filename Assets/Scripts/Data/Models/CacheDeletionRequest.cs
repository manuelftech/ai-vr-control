using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class CacheDeletionRequest
    {
        public List<ConversationIdProps> ConversationIds;
        
        public CacheDeletionRequest() { }
        public class Builder
        {
            private CacheDeletionRequest _build = new CacheDeletionRequest();
            public Builder ConversationIds(List<ConversationIdProps> conversationIds) { 
                _build.ConversationIds = conversationIds; 
                return this;
            }

            public CacheDeletionRequest Build()
            {
                return _build;
            }
        }
    }


     public class ConversationIdProps
    {
        public string ConversationId;
        
        public ConversationId() { }
        public class Builder
        {
            private ConversationIdProps _build = new ConversationIdProps();
            public Builder ConversationId(string conversationId) { 
                _build.ConversationId = conversationId; 
                return this;
            }
            public ConversationIdProps Build()
            {
                return _build;
            }
        }
    }
}