using System.Collections.Generic;
using System;

namespace AIControlVR.Data.Models
{
    [Serializable]
    public class TransformResponse
    {
        public string Tag;
        public List<ComponentSettings> Components;
        
        public TransformResponse() { }
        public class Builder
        {
            private TransformResponse _build = new TransformResponse();
            public Builder Tag(string tag)
            {
                 _build.Tag = tag;
                 return this;
            }
            public Builder Components(List<ComponentSettings> components)
            {
                if (_build.Components == null)
                {
                    _build.Components = new List<ComponentSettings>();
                }
                 _build.Components = components;
                 return this;
            }
            public TransformResponse Build()
            {
                return _build;
            }
        }
    }

    [Serializable]
    public class ComponentSettings
    {
        public string Component;
        public string State;
        
        public ComponentSettings() { }
        public class Builder
        {
            private ComponentSettings _build = new ComponentSettings();
            public Builder State(string state)
            {
                 _build.State = state;
                 return this;
            }
            public Builder Component(string component)
            {
                 _build.Component = component;
                 return this;
            }
            public ComponentSettings Build()
            {
                return _build;
            }
        }
    }




}