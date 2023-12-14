import { useState, useEffect, useRef, FC } from 'react'
import './App.css'
import classNames from 'classnames'
import _ from "lodash"

interface MessageProps {
  text: string,
  onIntersectionChange?: (visible: boolean) => void,
  charAspectRatio: number
  intersectionMargin?: string,
  className?: string,
  fit?: boolean,
}

export const Message: FC<MessageProps> = ({ text, onIntersectionChange, intersectionMargin, className, fit, charAspectRatio }) => {
  const ref = useRef<HTMLDivElement>(null)
  const [fitFontSize, setFitFontSize] = useState<number>()

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        onIntersectionChange && onIntersectionChange(entry.isIntersecting);
      },
      { rootMargin: intersectionMargin }
    );
    if(ref.current){
      observer.observe(ref.current)
      const frozenRef = ref.current
      return () => {
        if(ref.current){
          observer.unobserve(frozenRef)
        }
      }
    }
  }, [ref.current]);

  useEffect(() => {
    if(fit){
      let lines: string[] = text.split('\n');
      const longestLine = _.max(lines.map(l => l.length)) ?? 0
      setFitFontSize(((ref.current?.clientWidth ?? 0) - 40) / longestLine / charAspectRatio)
    }
  })

  return (
    <div
      className={classNames(className)}
      style={fit? {fontSize: fitFontSize} : {}}
    >
      <div style={{height: 1}} ref={ref}/>
      { text }
    </div>
  )
}
