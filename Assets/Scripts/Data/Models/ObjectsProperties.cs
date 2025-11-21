using System.Collections.Generic;
using System;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class ObjectsProperties
    {
        public List<ObjectProperties> VirtualRealityState;
        
        public ObjectsProperties() { }
    }

    [Serializable]
    public class ObjectProperties
    {
        public string Id ;
        public string Tag ;
        public string Name ;
        public ComponentsProperties Components;
        public TransformProperties Transform;
        public ObjectProperties() { }
    }

    [Serializable]
    public class ComponentsProperties
    {
        public CoordinatesProperties ConstantForce ;
        public string Color;
        public string Text;
        public ComponentsProperties() { }
    }

    [Serializable]
    public class TransformProperties
    {
        public CoordinatesProperties Position;
        public CoordinatesProperties Rotation;
        public CoordinatesProperties Scale;
        public TransformProperties() { }
        
    }

    [Serializable]
    public class CoordinatesProperties
    {
        public float X; // 1.98
        public float Y; // 1.287
        public float Z; // 0.03871146
        public CoordinatesProperties() { }
    }
}