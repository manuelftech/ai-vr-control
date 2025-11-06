using System;
using System.Collections.Generic;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class APIChatbotRequest
    {
        public string Prompt { get; set; }
        public ObjectsProperties? GameObjectsProperties { get; set; }
    }
}