using System;
using System.Collections.Generic;

namespace AIControlMagicVR.Data.Models
{
    [Serializable]
    public class ObjectsProperties
    {
        public List<ObjectProperties>? GameObjects ;
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
        public string Id ;
        public string Tag ; // cube
        public string Name ; // cube_4
        public ComponentsProperties? Components ;
        public TransformProperties? Transform ;
        public ObjectProperties() { }
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
            public ObjectPropertiesBuilder Name(string name)
            {
                _instance.Name = name;
                return this;
            }
            public ObjectPropertiesBuilder Components(ComponentsProperties components)
            {
                _instance.Components = components;
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
    public class ComponentsProperties
    {
        public CoordinatesProperties? ConstantForce ; // 9.84
        public string? Color ; // blue
        public ComponentsProperties() { }
        public static ComponentsPropertiesBuilder Builder()
        {
            return new ComponentsPropertiesBuilder();
        }

        public class ComponentsPropertiesBuilder
        {
            private ComponentsProperties _instance = new ComponentsProperties();
            public ComponentsPropertiesBuilder ConstantForce(CoordinatesProperties constantForce)
            {
                _instance.ConstantForce = constantForce;
                return this;
            }
            public ComponentsPropertiesBuilder Color(string color)
            {
                _instance.Color = color;
                return this;
            }
            public ComponentsProperties Build()
            {
                return _instance;
            }
        }
    }

    [Serializable]
    public class TransformProperties
    {
        public CoordinatesProperties? Position ;
        public CoordinatesProperties? Rotation ;
        public CoordinatesProperties? Scale ;

        public TransformProperties() { }
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
        public float? X ; // 1.98
        public float? Y ; // 1.287
        public float? Z ; // 0.03871146

        public CoordinatesProperties() { }
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