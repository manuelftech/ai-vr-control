using System;
using System.Collections.Generic;

namespace AIControlMagicVR.Data.Models
{

    [Serializable]
    public class ObjectsProperties
    {
        public List<ObjectsProperties> gameObjects;
    }

    [Serializable]
    public class ObjectProperties
    {
        public string instanceId { get; set; }
        public string tag { get; set; } // cube
        public float color { get; set; }
        public int constantForce { get; set; } // 9.83
        public int x { get; set; }
        public int y { get; set; }
        public int z { get; set; }
    }
}