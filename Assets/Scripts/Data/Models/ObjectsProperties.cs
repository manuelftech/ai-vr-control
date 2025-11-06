using System;
using System.Collections.Generic;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class ObjectsProperties
    {
        public List<ObjectProperties>? GameObjects { get; private set; }
        public ObjectsProperties() { }
        public static ObjectsPropertiesBuilder Builder()
        {
            return new ObjectsPropertiesBuilder();
        }

        public class ObjectsPropertiesBuilder
        {
            private ObjectsProperties _instance = new ObjectsProperties();
            public ObjectsPropertiesBuilder GameObjects(List<ObjectProperties> gameObjects)
            {
                _instance.GameObjects = gameObjects;
                return this;
            }
            public ObjectsProperties Build()
            {
                return _instance;
            }
        }
    }

    [Serializable]
    public class ObjectProperties
    {
        public string Id { get; set; }
        public string Tag { get; set; } // cube
        public ComponentProperties? Component { get; private set; }
        public TransformProperties? Transform { get; private set; }
        private ObjectProperties() { }
        public static ObjectPropertiesBuilder Builder()
        {
            return new ObjectPropertiesBuilder();
        }

        public class ObjectPropertiesBuilder
        {
            private ObjectProperties _instance = new ObjectProperties();
            public ObjectPropertiesBuilder Id(string id)
            {
                _instance.Id = id;
                return this;
            }
            public ObjectPropertiesBuilder Tag(string tag)
            {
                _instance.Tag = tag;
                return this;
            }
            public ObjectPropertiesBuilder Component(ComponentProperties component)
            {
                _instance.Component = component;
                return this;
            }
            public ObjectPropertiesBuilder Transform(TransformProperties transform)
            {
                _instance.Transform = transform;
                return this;
            }
            public ObjectProperties Build()
            {
                return _instance;
            }
        }
    }


    [Serializable]
    public class ComponentProperties
    {
        public CoordinatesProperties? ConstantForce { get; private set; } // 9.84
        public string? Color { get; private set; } // blue
        private ComponentProperties() { }
        public static ComponentPropertiesBuilder Builder()
        {
            return new ComponentPropertiesBuilder();
        }

        public class ComponentPropertiesBuilder
        {
            private ComponentProperties _instance = new ComponentProperties();
            public ComponentPropertiesBuilder ConstantForce(CoordinatesProperties constantForce)
            {
                _instance.ConstantForce = constantForce;
                return this;
            }
            public ComponentPropertiesBuilder Color(string color)
            {
                _instance.Color = color;
                return this;
            }
            public ComponentProperties Build()
            {
                return _instance;
            }
        }
    }

    [Serializable]
    public class TransformProperties
    {
        public CoordinatesProperties? Position { get; private set; }
        public CoordinatesProperties? Rotation { get; private set; }
        public CoordinatesProperties? Scale { get; private set; }

        private TransformProperties() { }
        public static TransformPropertiesBuilder Builder()
        {
            return new TransformPropertiesBuilder();
        }

        public class TransformPropertiesBuilder
        {
            private TransformProperties _instance = new TransformProperties();
            public TransformPropertiesBuilder Position(CoordinatesProperties position)
            {
                _instance.Position = position;
                return this;
            }
            public TransformPropertiesBuilder Rotation(CoordinatesProperties rotation)
            {
                _instance.Rotation = rotation;
                return this;
            }

            public TransformPropertiesBuilder Scale(CoordinatesProperties scale)
            {
                _instance.Scale = scale;
                return this;
            }
            public TransformProperties Build()
            {
                return _instance;
            }
        }
    }

    [Serializable]
    public class CoordinatesProperties
    {
        public float? X { get; private set; } // 1.98
        public float? Y { get; private set; } // 1.287
        public float? Z { get; private set; } // 0.03871146

        private CoordinatesProperties() { }
        public static CoordinatesPropertiesBuilder Builder()
        {
            return new CoordinatesPropertiesBuilder();
        }
        public class CoordinatesPropertiesBuilder
        {
            private CoordinatesProperties _instance = new CoordinatesProperties();
            public CoordinatesPropertiesBuilder X(float x)
            {
                _instance.X = x;
                return this;
            }
            public CoordinatesPropertiesBuilder Y(float y)
            {
                _instance.Y = y;
                return this;
            }

            public CoordinatesPropertiesBuilder Z(float z)
            {
                _instance.Z = z;
                return this;
            }
            public CoordinatesProperties Build()
            {
                return _instance;
            }
        }
    }

}