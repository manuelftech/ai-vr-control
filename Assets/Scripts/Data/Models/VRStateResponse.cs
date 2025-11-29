using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class VRStateResponse
    {
        public string Tag;
        public List<VRProperty> Properties;
        
        public VRStateResponse() { }
        public class Builder
        {
            private VRStateResponse _build = new VRStateResponse();
            public Builder Tag(string tag)
            {
                 _build.Tag = tag;
                 return this;
            }
            public Builder Properties(List<VRProperty> properties)
            {
                if (_build.Properties == null)
                {
                    _build.Properties = new List<VRProperty>();
                }
                 _build.Properties = properties;
                 return this;
            }
            public VRStateResponse Build()
            {
                return _build;
            }
        }
    }

    [Serializable]
    public class VRProperty
    {
        public string Name;
        public string State;
        
        public VRProperty() { }
        public class Builder
        {
            private VRProperty _build = new VRProperty();
            public Builder Name(string name)
            {
                 _build.Name = name;
                 return this;
            }
            public Builder State(string state)
            {
                 _build.State = state;
                 return this;
            }
            public VRProperty Build()
            {
                return _build;
            }
        }
    }




}