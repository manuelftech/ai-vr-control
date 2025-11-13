using System;
using System.Collections.Generic;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class APIChatbotRequest
    {
        public string Prompt { get; private set; }
        public List<ObjectProperties>? VirtualRealityState { get; private set; }
        private APIChatbotRequest() { }
        
        public static APIChatbotRequestBuilder Builder()
        {
            return new APIChatbotRequestBuilder();
        }

        public class APIChatbotRequestBuilder
        {
            private APIChatbotRequest _instance = new APIChatbotRequest();
            public APIChatbotRequestBuilder Prompt(string prompt)
            {
                _instance.Prompt = prompt;
                return this;
            }

            public APIChatbotRequestBuilder VirtualRealityState(List<ObjectProperties> virtualRealityState)
            {
                _instance.VirtualRealityState = virtualRealityState;
                return this;
            }

            public APIChatbotRequest Build()
            {
                return _instance;
            }
        }
    }
}