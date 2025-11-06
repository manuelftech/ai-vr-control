using System;
using System.Collections.Generic;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class APIChatbotRequest
    {
        public string Prompt { get; private set; }
        public ObjectsProperties? GameObjectsProperties { get; private set; }
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
            }

            public APIChatbotRequestBuilder GameObjectsProperties(ObjectsProperties gameObjectsProperties)
            {
                _instance.GameObjectsProperties = gameObjectsProperties;
            }

            public APIChatbotRequest Build()
            {
                return _instance;
            }
        }
    }
}