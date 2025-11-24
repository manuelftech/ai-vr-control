using System.Collections.Generic;
using System;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class ObjectsProperties
    {
        public List<ObjectProperties> VirtualRealityState;
        
        public ObjectsProperties() { }
        public class Builder
        {
            private ObjectsProperties _build = new ObjectsProperties();
            public Builder VirtualRealityState(List<ObjectProperties> VirtualRealityState)
            {
                if (_build.VirtualRealityState == null)
                {
                    _build.VirtualRealityState = new List<ObjectProperties>();
                }
                 _build.VirtualRealityState = VirtualRealityState;
                 return this;
            }
            public ObjectsProperties Build()
            {
                return _build;
            }
        }
    }

    [Serializable]
    public class ObjectProperties
    {
        public string Id;
        public string Tag;
        public string Name;
        public ComponentsProperties Components;
        public TransformProperties Transform;

        public ObjectProperties() { }
        public class Builder
        {
            private ObjectProperties _build = new ObjectProperties();
            public Builder Id(string id) { 
                _build.Id = id; 
                return this;
            }
            public Builder Tag(string tag) { 
                _build.Tag = tag; 
                return this;
            }
            public Builder Name(string name) { 
                _build.Name = name; 
                return this;
            }
            public Builder Components(ComponentsProperties components) { 
                _build.Components = components; 
                return this;
            }
            public Builder Transform(TransformProperties transform) { 
                _build.Transform = transform; 
                return this;
            }
            public ObjectProperties Build()
            {
                return _build;
            }
        }
    }

    [Serializable]
    public class ComponentsProperties
    {
        public CoordinatesProperties ConstantForce ;
        public string Color;
        public string Text;

        public ComponentsProperties() { }
        public class Builder
        {
            private ComponentsProperties _build = new ComponentsProperties();
            public Builder ConstantForce(CoordinatesProperties constantForce) { 
                _build.ConstantForce = constantForce; 
                return this;
            }
            public Builder Color(string color) { 
                _build.Color = color; 
                return this;
            }
            public Builder Text(string text) { 
                _build.Text = text; 
                return this;
            }
            public ComponentsProperties Build()
            {
                return _build;
            }
        }
    }

    [Serializable]
    public class TransformProperties
    {
        public CoordinatesProperties Position;
        public CoordinatesProperties Rotation;
        public CoordinatesProperties Scale;

        public TransformProperties() { }
        public class Builder
        {
            private TransformProperties _build = new TransformProperties();
            public Builder Position(CoordinatesProperties position) { 
                _build.Position = position; 
                return this;
            }
            public Builder Rotation(CoordinatesProperties rotation) { 
                _build.Rotation = rotation; 
                return this;
            }
            public Builder Scale(CoordinatesProperties scale) { 
                _build.Scale = scale; 
                return this;
            }
            public TransformProperties Build()
            {
                return _build;
            }
        }
    }

    [Serializable]
    public class CoordinatesProperties
    {
        public float X;
        public float Y;
        public float Z;

        public CoordinatesProperties() { }
        public class Builder
        {
            private CoordinatesProperties _build = new CoordinatesProperties();
            public Builder X(float x) { 
                _build.X = x; 
                return this;
            }
            public Builder Y(float y) { 
                _build.Y = y; 
                return this;
            }
            public Builder Z(float z) { 
                _build.Z = z; 
                return this;
            }
            public CoordinatesProperties Build()
            {
                return _build;
            }
        }
    }
}