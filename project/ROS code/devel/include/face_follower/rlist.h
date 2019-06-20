// Generated by gencpp from file face_follower/rlist.msg
// DO NOT EDIT!


#ifndef FACE_FOLLOWER_MESSAGE_RLIST_H
#define FACE_FOLLOWER_MESSAGE_RLIST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>

namespace face_follower
{
template <class ContainerAllocator>
struct rlist_
{
  typedef rlist_<ContainerAllocator> Type;

  rlist_()
    : header()
    , data()  {
    }
  rlist_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , data(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef std::vector<float, typename ContainerAllocator::template rebind<float>::other >  _data_type;
  _data_type data;





  typedef boost::shared_ptr< ::face_follower::rlist_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::face_follower::rlist_<ContainerAllocator> const> ConstPtr;

}; // struct rlist_

typedef ::face_follower::rlist_<std::allocator<void> > rlist;

typedef boost::shared_ptr< ::face_follower::rlist > rlistPtr;
typedef boost::shared_ptr< ::face_follower::rlist const> rlistConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::face_follower::rlist_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::face_follower::rlist_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace face_follower

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': True}
// {'face_follower': ['/home/yuyu/Openni/src/face_follower/msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::face_follower::rlist_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::face_follower::rlist_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::face_follower::rlist_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::face_follower::rlist_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::face_follower::rlist_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::face_follower::rlist_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::face_follower::rlist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a120344537a3b099cc9ec9957d4619fc";
  }

  static const char* value(const ::face_follower::rlist_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa120344537a3b099ULL;
  static const uint64_t static_value2 = 0xcc9ec9957d4619fcULL;
};

template<class ContainerAllocator>
struct DataType< ::face_follower::rlist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "face_follower/rlist";
  }

  static const char* value(const ::face_follower::rlist_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::face_follower::rlist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "Header header\n\
float32[] data\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n\
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
";
  }

  static const char* value(const ::face_follower::rlist_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::face_follower::rlist_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.data);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct rlist_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::face_follower::rlist_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::face_follower::rlist_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "data[]" << std::endl;
    for (size_t i = 0; i < v.data.size(); ++i)
    {
      s << indent << "  data[" << i << "]: ";
      Printer<float>::stream(s, indent + "  ", v.data[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // FACE_FOLLOWER_MESSAGE_RLIST_H
