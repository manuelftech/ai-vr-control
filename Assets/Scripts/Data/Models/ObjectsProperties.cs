using System;
using System.Collections.Generic;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class ObjectsProperties
    {
        public List<ObjectProperties>? GameObjects { get; set; }
    }

    [Serializable]
    public class ObjectProperties
    {
        public required string Id { get; set; }
        public required string Tag { get; set; } // cube
        public ComponentsProperties? Component { get; set; }
        public TransformProperties? Transform { get; set; }
    }

    [Serializable]
    public class ComponentsProperties
    {
        public CoordinatesProperties? ConstantForce { get; set; } // 9.84
        public string? Color { get; set; } // blue
    }

    [Serializable]
    public class TransformProperties
    {
        public CoordinatesProperties? Position { get; set; }
        public CoordinatesProperties? Rotation { get; set; }
        public CoordinatesProperties? Scale { get; set; }
    }

    [Serializable]
    public class CoordinatesProperties
    {
        public float? X { get; set; } // 1.98
        public string? Y { get; set; } // 1.287
        public string? Z { get; set; } // 0.03871146
    }

}