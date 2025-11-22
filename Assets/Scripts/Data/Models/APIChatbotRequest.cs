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
    }
}