using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class APIChatbotRequest
    {
        public string Prompt;
        
        public APIChatbotRequest() { }
        public class Builder
        {
            private APIChatbotRequest _build = new APIChatbotRequest();
            public Builder Prompt(string prompt) { 
                _build.Prompt = prompt; 
                return this;
            }

            public APIChatbotRequest Build()
            {
                return _build;
            }
        }
    }
}