using System.Collections.Generic;
using System;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class APIChatbotRequest
    {
        public string Prompt;
        public List<ObjectProperties> VirtualRealityState;
        
        public APIChatbotRequest() { }
        public class Builder
        {
            private APIChatbotRequest _build = new APIChatbotRequest();
            public Builder Prompt(string prompt) { 
                _build.Prompt = prompt; 
                return this;
            }
            public Builder VirtualRealityState(List<ObjectProperties> virtualRealityState) { 
                _build.VirtualRealityState = virtualRealityState; 
                return this;
            }

            public APIChatbotRequest Build()
            {
                return _build;
            }
        }
    }
}